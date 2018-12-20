import musicbrainzngs, xml
import MySQLdb as MariaDB

conn = MariaDB.connect(user='simon', passwd='phaedra74', db='catalogue', use_unicode=True, charset='utf8')
musicbrainzngs.set_useragent("Simon's CD Collection DB", "1.0")
musicbrainzngs.auth("ecomusicaddict","3amatBotMfO")

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

def extract_label(label_info_list):
    if 'label' in label_info_list:
        return label_info_list['label']['name']
    else:
        return None

def find_artist_mbid(artistname):
    for i in range(1,6):
        try:
            searchresults = musicbrainzngs.search_artists(artistname, strict=True)
        except:
            if i < 5:
                continue
            else:
                raise
            break

    for result in searchresults['artist-list']:
        if result['ext:score'] == '100':
            return result['id']


def get_artist_record(mbid):
    for i in range(1,6):
        try:
            artrecord = musicbrainzngs.get_artist_by_id(mbid, includes=["artist-rels", "aliases"])
        except (musicbrainzngs.NetworkError, musicbrainzngs.ResponseError):
            if i < 5:
                continue
            else:
                raise
        break

    return artrecord



def update_artists():
    #sql = "TRUNCATE TABLE relationship;"
    #c = conn.cursor()
    #c.execute(sql)
    #conn.commit()

    sql = "SELECT DISTINCT artistid, artistname FROM artist where country is null;"
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()

    for r in results:
        artistid = r[0]
        artistname = r[1]
        mbid = find_artist_mbid(artistname)
        artrecord = get_artist_record(mbid)['artist']
        print(artrecord)
        if 'country' in artrecord:
            print("{} - {}".format(artistname, artrecord['country']))
            sql = "UPDATE artist set Country='{}' WHERE artistid={}".format(artrecord['country'], artistid)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()

        """
        if 'artist-relation-list' in artrecord['artist']:
            art = artrecord['artist']['artist-relation-list']
            for arl in art:
                if 'type' in arl and arl['type'] == 'supporting musician':
                    assoc_artist = arl['artist']['name']
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

                        sql = "INSERT INTO relationship (artistid_parent, artistid_child, startdate, enddate, support)" \
                              "VALUES ({}, {}, {}, {}, 'Y')".format(artistid, assoc_id,
                                                               'NULL' if begin is None else begin,
                                                               'NULL' if end is None else end)
                        c = conn.cursor()
                        c.execute(sql)
                        conn.commit()
                        print("--- ADDED SUPPORT: {} -> {} ({}-{})".format(artistname, assoc_artist,
                                                        '' if begin is None else begin,
                                                        '' if end is None else end))
                    else:
                        print("Not found: {}".format(assoc_artist))
        """

mbid = find_artist_mbid("Isao Tomita")
art_record = get_artist_record(mbid)
print(art_record)

