import musicbrainzngs as MBrainz

MBrainz.set_useragent("CatDB Test Scripts", "1.0")
searchartist = "Jon Thor Birgisson"

def print_artist(artist_details):
    for k, v in artist_details.items():
        if k not in ['artist-relation-list', 'area', 'alias-list']:
            print("{}: {}".format(k, v))

def print_aliases(artist_aliases):
    for alias in artist_aliases:
        related_to = alias['alias']
        print("\t{}: {}".format("Alias", related_to))

def print_relations(artist_relations):
    for relation in artist_relations:
        type = relation['type']
        related_to = relation['artist']['name']
        print("\t{}: {}".format(type, related_to))


def parse_artistrecord(artist_mbid):
    artistrecord = MBrainz.get_artist_by_id(artist_mbid, includes=['aliases', 'artist-rels'])
    artist_details = artistrecord['artist']
    print_artist(artist_details)

    if 'artist-relation-list' in artist_details:
        artist_relations = artist_details['artist-relation-list']
        print_relations(artist_relations)

    if 'alias-list' in artist_details:
        artist_aliases = artist_details['alias-list']
        print_aliases(artist_aliases)


def main():
    searchresults = MBrainz.search_artists(searchartist)

    for result in searchresults['artist-list']:
        id = result['id']
        if result['ext:score'] == "100":
            parse_artistrecord(id)

if __name__ == '__main__':
    main()