import musicbrainzngs
import MySQLdb as MariaDB

conn = MariaDB.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')
musicbrainzngs.set_useragent("Simon's CD Collection DB", "1.0")
musicbrainzngs.auth("ecomusicaddict","3amatBotMfO")

def get_data():
    sql = "select albumid, artist.ArtistName, yearreleased, album " \
          "from album inner join artist on artist.artistid = album.artistid " \
          "where artistcredit is null order by albumid;"
    c = conn.cursor()
    c.execute(sql)
    return c.fetchall()

def get_album_mbid(artistname, album, yearreleased):
    searchresults = musicbrainzngs.search_release_groups(artist=artistname, release=album)
    for result in searchresults['release-group-list']:
        if result['ext:score']=='100':
            return result['id']
    return None

def get_release_record(mbid):
    return musicbrainzngs.get_release_group_by_id(mbid, includes=['artists'])['release-group']

def make_safe(text):
    return text.replace("'","''")

def find_artist_id(artistname, artist_mbid):
    sql = "select artistid from artist_copy where artistname='{}'".format(make_safe(artistname))
    c = conn.cursor()
    rowcount = c.execute(sql)
    if rowcount > 0:
        return c.fetchone()[0]
    else:
        artistrecord = musicbrainzngs.get_artist_by_id(artist_mbid)['artist']
        sortname = artistrecord['sort-name']
        isgroup = 1 if 'type' not in artistrecord or artistrecord['type'] == 'Group' else 0
        sql = "INSERT INTO artist_copy(artistname, sortname, `group`, mbid) VALUES ('{}', '{}', {}, '{}');".format(make_safe(artistname),
                                                                                                make_safe(sortname),
                                                                                                isgroup, artist_mbid)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        return c.lastrowid

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

def get_artist_record(mbid):
    for i in range(1,6):
        try:
            artrecord = musicbrainzngs.get_artist_by_id(mbid, includes=["artist-rels"])
        except (musicbrainzngs.NetworkError, musicbrainzngs.ResponseError):
            if i < 5:
                continue
            else:
                raise
        break

    return artrecord

def get_artist_name(mbid):
    art_record = musicbrainzngs.get_artist_by_id(mbid, includes='aliases')
    if 'alias-list' in art_record['artist']:
        for alias in art_record['artist']['alias-list']:
            if 'locale' in alias:
                if alias['locale'] == 'en' and 'primary' in alias:
                    return alias['alias']
    return art_record['artist']['name']

def parse_artist(release_record, albumid):
    artistcredit = ""
    if 'artist-credit' in release_record:
        artistlist = release_record['artist-credit']
        for artist in artistlist:
            if 'artist' in artist:
                artist_mbid = artist['artist']['id']
                artistname = get_artist_name(artist_mbid)
                artistcredit += artistname
                artistid = find_artist_id(artistname, artist_mbid)
                if not albumartist_exists(albumid, artistid):
                    insert_albumartist(albumid, artistid)
            else:
                artistcredit += artist
    return artistcredit


def main():
    data_rows = get_data()
    for row in data_rows:
        albumid, artistname, yearreleased, album = row[0:4]
        print("Processing: {} - {}".format(artistname, album))
        mbid = get_album_mbid(artistname, album, yearreleased)
        release_record = get_release_record(mbid)
        artistcredit = parse_artist(release_record, albumid)
        update_artistcredit(albumid, artistcredit)

if __name__ == '__main__':
    main()