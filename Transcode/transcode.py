#!/usr/bin/python3

from mutagen import flac, mp3
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from multiprocessing import Pool
from datetime import datetime, timedelta

import os
import shutil
import scan
import re


#basedir = "c:/users/h687era/downloads/temp/Incoming"
#musicdir = "c:/users/h687era/downloads/temp/output/"
#archivedir = "c:/users/h687era/downloads/temp/archive/"

basedir = "/home/simon/Rips/Incoming/"
musicdir = "/home/simon/Rips/Temp/"
archivedir = "/home/simon/FLAC/"


def retrieve_numerics(src):
    numerics = re.findall("\d+", src)
    return int(numerics[0])


def prep_dirs():
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".flac"):

                ff = None
                ff = flac.FLAC(os.path.join(basedir, f))

                t = ff.tags

                albumartist = t["ALBUMARTIST"][0]
                album = t["Album"][0]

                if albumartist[-1:] == ".":
                    albumartist = albumartist[:-1] + "_"

                if album[-1:] == ".":
                    album = album[:-1] + "_"

                year = str(t["originalyear"][0])

                for xdir in [musicdir, archivedir]:
                    artistdir = os.path.join(xdir, make_safe(albumartist))
                    albumdir = os.path.join(artistdir, "{} - {}".format(year, make_safe(album)))
                    for d in [artistdir, albumdir]:
                        if not os.path.exists(d):
                            print("Creating dir for {} - {}".format(albumartist, album))
                            os.mkdir(d)


def determine_dest_file(basedir, extension, albumartist, albumtitle, discno, trackno, tracktitle, year):

    if albumartist[-1:] == ".":
        albumartist = albumartist[:-1] + "_"

    if albumtitle[-1:] == ".":
        albumtitle = albumtitle[:-1] + "_"

    dest_file = "{}.{} {}.{}".format(discno, trackno, tracktitle, extension)
    dest_file = make_safe(dest_file)
    dest_file = os.path.join(basedir, make_safe(albumartist), "{} - {}".format(year, make_safe(albumtitle)), dest_file)
    return dest_file


def make_safe(filename):
    chars_to_remove = "< > \\ / | ? *".split()

    for c in chars_to_remove:
        filename = filename.replace(c, "")
    filename = filename.replace(":", ";")
    filename = filename.replace("\"", "'")
    filename = filename.replace("$", "S")
    return filename


def process(source_file):

    f = None

    f = flac.FLAC(source_file)

    t = f.tags

    albumartist = t["ALBUMARTIST"][0]
    album = t["Album"][0]

    year = str(t["originalyear"][0])

    disc = str(retrieve_numerics(t["DISCNUMBER"][0])).zfill(2)
    track = str(retrieve_numerics(t["tracknumber"][0])).zfill(2)
    tracktitle = t["title"][0]
    length_hr = int(f.info.length / 3600)
    length_min = int((f.info.length - (length_hr * 3600)) / 60)
    length_sec = int(f.info.length) % 60
    length = "{:02d}{:02d}{:02d}".format(length_hr, length_min, length_sec)

    dest_file = determine_dest_file(musicdir, "ogg", albumartist, album, disc, track, tracktitle, year)

    timestart = datetime.now()
    command = "oggenc --quiet -q4 \"{}\" -o \"{}\"".format(source_file, dest_file)
    os.system(command)

    arc_file = determine_dest_file(archivedir, "flac", albumartist, album, disc, track, tracktitle, year)
    shutil.move(source_file, arc_file)

    timeend = datetime.now()

    timetaken = timeend - timestart
    speed = f.info.length / timetaken.total_seconds()
    print("Transcoded >> {}: {} - {:.2f}s {:.2f}x".format(albumartist, tracktitle,
                                                                  timetaken.total_seconds(), speed))


def run():

    prep_dirs()
    filelist = []
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".flac"):
                file = os.path.join(root, f)
                filelist.append(file)

    p = Pool(4)
    sortedfilelist = sorted(filelist, key=str.lower)
    dummy = p.map(process, sortedfilelist)

    scan.scan(musicdir)
    os.system("cp -r /home/simon/Rips/Temp/* /home/simon/Music/")
    os.system("rm -r /home/simon/Rips/Temp/*")

if __name__ == '__main__':
    run()
