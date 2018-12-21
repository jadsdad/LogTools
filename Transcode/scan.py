#!/usr/bin/python3

import MySQLdb as MariaDB
from mutagen import oggvorbis
import re
import os
import musicbrainzngs as MBrainz


conn = MariaDB.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')
MBrainz.set_useragent("Simon's Collection Database", "1.0")
#MBrainz.set_hostname("beta.musicbrainz.org")
MBrainz.auth("ecomusicaddict", "3amatBotMfO")

def retrieve_numerics(src):
    numerics = re.findall("\d+", src)
    return int(numerics[0])

def find_artistid(artistname):
    artistname = artistname.replace("'","''")
    artistname = artistname.replace("’","''")
    sql = "SELECT artistid FROM artist where artistname='{}';".format(artistname)
    c = conn.cursor()
    rowcount = c.execute(sql)
    if rowcount > 0:
        row = c.fetchone()
        return row[0]
    else:
        return None

def find_artistidbymbid(mbid):
    sql = "SELECT artistid, `Group` FROM artist where mbid='{}';".format(mbid)
    c = conn.cursor()
    rowcount = c.execute(sql)
    if rowcount > 0:
        row = c.fetchone()
        return row[0], row[1] == b'\x01'
    else:
        return None, None

def obtain_artist_mbid(artistname):
    searchresults = MBrainz.search_artists(artist=artistname, strict=True)
    for result in searchresults['artist-list']:
        if result['ext:score'] == "100":
            return result['id']

    return None

def relationship_exists(parentid, childid, startdate, enddate):
    sql = "SELECT relationshipid FROM relationship " \
          "where artistid_parent = {} AND artistid_child = {} " \
          "and startdate{} and enddate{}".format(parentid, childid,
                                                   ' is NULL' if startdate is None else " =" + startdate,
                                                   ' is NULL' if enddate is None else " = " + enddate)
    c = conn.cursor()
    rowcount = c.execute(sql)
    return rowcount > 0

def obtain_relationships(mbid):
    if mbid is not None:
        artrecord = MBrainz.get_artist_by_id(mbid, includes=["artist-rels"])
        artistid, isgroup = find_artistidbymbid(mbid)

        if 'artist-relation-list' in artrecord['artist']:
            artistname = artrecord['artist']['name']
            art = artrecord['artist']['artist-relation-list']
            for arl in art:
                if 'type' in arl and arl['type'] in ['member of band', 'collaboration']:
                    assoc_artist = arl['artist']['name']
                    print("Association found with " + assoc_artist)
                    assoc_id = find_artistid(assoc_artist)
                    if assoc_id is not None:
                        if 'begin' in arl:
                            begin = arl['begin'][:4]
                        else:
                            begin = None

                        if 'end' in arl:
                            end = arl['end'][:4]
                        else:
                            end = None

                        if isgroup:
                            add_relationship(assoc_id, artistid, begin, end)
                        else:
                            add_relationship(artistid, assoc_id, begin, end)

def add_relationship(parentid, childid, startdate, enddate):
    if not relationship_exists(parentid, childid, startdate, enddate):
        sql = "INSERT INTO relationship (artistid_parent, artistid_child, startdate, enddate) " \
              "VALUES ({}, {}, {}, {})".format(parentid, childid,
                                               'NULL' if startdate is None else startdate,
                                               'NULL' if enddate is None else enddate)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        print("Relationship added - #{} to #{}".format(parentid, childid))



def obtain_sortname(artistname):
    is_group = False
    mbid = obtain_artist_mbid(artistname)
    if mbid is not None:
        artistrecord = MBrainz.get_artist_by_id(mbid)['artist']
        is_group = artistrecord['type'] == "Group"
        return artistrecord['sort-name'], is_group
    else:
        return artistname, True

def make_safe(s):
    return s.replace("'", "''")

def scan(basedir):
    release_ids = {}
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".ogg"):
                filename = os.path.join(root, f)
                f = oggvorbis.OggVorbis(filename)
                t = f.tags
                album_artist = t["ALBUMARTIST"][0]
                album = t["Album"][0]
                year = str(t["originalyear"][0])
                disc = str(retrieve_numerics(t["DISCNUMBER"][0]))
                track = str(retrieve_numerics(t["tracknumber"][0]))
                title = t["title"][0]

                print("Scanning > {} - {}".format(album, title))

                length_hr = int(f.info.length / 3600)
                length_min = int((f.info.length - (length_hr * 3600)) / 60)
                length_sec = int(f.info.length) % 60
                length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)
                filesize = os.path.getsize(filename)
                bitrate = f.info.bitrate
                if 'MUSICBRAINZ_RELEASEGROUPID' in t:
                    album_mbid = t["MUSICBRAINZ_RELEASEGROUPID"][0]
                else:
                    album_mbid = get_album_mbid(album_artist, album)

                albumid = getAlbumID(album, year, album_artist)
                removeStream(albumid)

                if albumid not in release_ids:
                    release_ids[albumid] = album_mbid
                insertTrack(albumid, disc, track, title, length, filesize, bitrate, filename)

    for albumid, album_mbid in release_ids.items():
        release_record = get_release_record(album_mbid)
        parse_artist(release_record, albumid)

    cursor = conn.cursor()
    procs = ["do_remap", "playcount_audit"]

    #for p in procs:
    #    cursor.execute("CALL {};".format(p))
    #    conn.commit()

def get_release_record(mbid):
    successful = False
    print("Obtaining release record for MBID {}".format(mbid))
    while not successful:
        try:
            release_record = MBrainz.get_release_group_by_id(mbid, includes=['artists'])['release-group']
            successful = True
            return release_record
        except (MBrainz.NetworkError, MBrainz.ResponseError):
            print("Failed to get Release Record from MB. Retrying")



def get_album_mbid(artistname, album):
    searchresults = MBrainz.search_release_groups(artist=artistname, release=album)
    for result in searchresults['release-group-list']:
        if result['ext:score']=='100':
            return result['id']
    return None

def get_artist_name(mbid):
    successful = False
    print("Obtaining artist record for MBID {}".format(mbid))
    while not successful:
        try:
            art_record = MBrainz.get_artist_by_id(mbid, includes='aliases')
            successful = True
        except (MBrainz.NetworkError, MBrainz.ResponseError):
            print("Failed to get Artist Record from MB. Retrying")

    if 'alias-list' in art_record['artist']:
        for alias in art_record['artist']['alias-list']:
            if 'locale' in alias:
                if alias['locale'] == 'en' and 'primary' in alias:
                    return alias['alias']
    return art_record['artist']['name']

def find_artist_id(artistname, artist_mbid):
    sql = "select artistid from artist where mbid='{}'".format(artist_mbid)
    c = conn.cursor()
    rowcount = c.execute(sql)
    if rowcount > 0:
        return c.fetchone()[0]
    else:
        artistrecord = MBrainz.get_artist_by_id(artist_mbid)['artist']
        sortname = artistrecord['sort-name']
        isgroup = 1 if 'type' not in artistrecord or artistrecord['type'] == 'Group' else 0
        sql = "INSERT INTO artist(artistname, sortname, `group`, mbid) VALUES ('{}', '{}', {}, '{}');".format(make_safe(artistname),
                                                                                                make_safe(sortname),
                                                                                                isgroup, artist_mbid)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        return c.lastrowid

def parse_artist(release_record, albumid):
    artistcredit = ""
    if 'artist-credit' in release_record:
        artistlist = release_record['artist-credit']
        for artist in artistlist:
            if 'artist' in artist:
                artist_mbid = artist['artist']['id']
                artistname = get_artist_name(artist_mbid)
                print("MusicBrainz Artist: " + artistname)
                artistcredit += artistname
                artistid = find_artist_id(artistname, artist_mbid)
                if not albumartist_exists(albumid, artistid):
                    insert_albumartist(albumid, artistid)
                obtain_relationships(artist_mbid)
            else:
                artistcredit += artist

    print("\tArtist Credit: " + artistcredit)
    update_artistcredit(albumid, artistcredit)

def update_artistcredit(albumid, artistcredit):
    sql = "UPDATE album SET ArtistCredit = '{}' WHERE albumid={};".format(make_safe(artistcredit), albumid)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()

def albumartist_exists(albumid, artistid):
    sql = "SELECT * FROM albumartist where albumid = {} and artistid = {};;".format(albumid, artistid)
    c = conn.cursor()
    rowcount = c.execute(sql)
    return rowcount > 0

def insert_albumartist(albumid, artistid):
    sql = "INSERT INTO albumartist(albumid, artistid) VALUES ({},{});".format(albumid, artistid)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()

def getAlbumID(album, year, albumartist):
    cursor = conn.cursor()
    sql = "SELECT albumid FROM album WHERE album='{}' AND artistcredit = '{}' " \
          "AND yearreleased={};".format(make_safe(album), make_safe(albumartist), year)
    result = cursor.execute(sql)
    if result == 0:
        sql = "INSERT INTO album (album, yearreleased, albumtypeid, audit, artistcredit) " \
              "VALUES ('{}', {}, 12, 1, '{}');".format(make_safe(album), year, make_safe(albumartist))
        cursor.execute(sql)
        conn.commit()
        return cursor.lastrowid
    else:
        row = cursor.fetchone()
        return row[0]

def removeStream(albumid):
    cursor = conn.cursor()
    sql = "UPDATE album SET AlbumTypeID=12, SourceID=NULL where albumid={};".format(albumid)
    cursor.execute(sql)
    conn.commit()


def getTrackID(albumid, disc, track):
    cursor = conn.cursor()
    sql = "SELECT trackid FROM track WHERE albumid={} AND disc={} and track={};".format(albumid, disc, track)
    result = cursor.execute(sql)
    if result == 0:
        return 0
    else:
        return cursor.fetchone()[0]

def insertTrack(albumid, disc, track, title, length, size, bitrate, loc):
    cursor = conn.cursor()
    trackid = getTrackID(albumid, disc, track)

    if trackid == 0:
        cursor.execute("INSERT INTO track (albumid, disc, track, tracktitle, "
                       "length, audit, bitrate, size) VALUES ({}, {}, {}, '{}', '{}', 1, {}, {});".format(albumid, disc, track,
                                                                                 make_safe(title), length, bitrate, size))
    else:
        cursor.execute("UPDATE track SET audit=1, tracktitle = '{}', length = '{}', size = {}, bitrate = {} "
                       "WHERE trackid = {}".format(make_safe(title), length, size, bitrate, trackid))

    conn.commit()

if __name__ == '__main__':
    #scan("D:\\opus\\Jon Anderson\\1976 - Olias of Sunhillow\\")
    scan("/home/simon/Rips/Temp/")
