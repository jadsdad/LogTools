#!/usr/bin/python3

from mutagen import flac
from multiprocessing import Pool
import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets

basedir = "/home/simon/Rips/Transcode/"
musicdir = "/home/simon/Music/"
tempdir = "/home/simon/Rips/Temp/"


class TranscodeFile():

    def __init__(self, input_filename):
        self.__input = ""
        self.__output = ""
        self.album_artist = ""
        self.album_title = ""
        self.track_title = ""
        self.year = ""
        self.__output_dir = ""
        self.setInputFile(input_filename)

    @staticmethod
    def makeSafe(inString):
        chars_to_replace = ["\"", ":", "?", "/", "\\"]
        outstring = inString
        for c in chars_to_replace:
            outstring = outstring.replace(c, "")

        return outstring

    def setInputFile(self, input_file):
        self.__input = input_file

        f = os.path.basename(self.__input)
        ff = flac.FLAC(self.__input)
        tags = ff.tags

        self.album_artist = tags['ALBUMARTIST'][0]
        self.album_title = tags['ALBUM'][0]
        self.track_title = tags['TITLE'][0]
        self.year = tags['DATE'][0]

        self.__album_artist_safe = self.makeSafe(self.album_artist)
        self.__album_title_safe = self.makeSafe(self.album_title)
        artist_dir = os.path.join(tempdir, self.__album_artist_safe)
        self.__output_dir = os.path.join(artist_dir, "{} ({})".format(self.__album_title_safe,
                                                                      self.year))
        if not os.path.exists(artist_dir):
            os.mkdir(artist_dir)

        if not os.path.exists(self.__output_dir):
            os.mkdir(self.__output_dir)

        self.__output = os.path.join(self.__output_dir, f.replace(".flac", ".ogg"))

    def doTranscode(self):
        command = "oggenc -Q -q6 \"{}\" -o \"{}\"".format(self.__input, self.__output)
        print("Transcoding >> {}: {}".format(self.album_artist, self.track_title))
        os.system(command)


def run_me(t):
    t.doTranscode()


def main():
    print("Scanning...")
    filestoencode = []
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".flac"):
                ff = TranscodeFile(os.path.join(root, f))
                filestoencode.append(ff)
                print("Found >> {}: {}".format(ff.album_artist, ff.track_title))

    p = Pool(4)
    p.map(run_me, filestoencode)

    print("Calculating ReplayGain")
    os.system("vorbisgain -a -q -r {}*".format(tempdir))

    print("Finishing up")
    os.system("cp -rl /home/simon/Rips/Temp/* /home/simon/Music/")
    os.system("cp -rl /home/simon/Rips/Transcode/* /home/simon/Rips/Scan/")
    os.system("rm -r /home/simon/Rips/Temp/*")
    os.system("rm -r /home/simon/Rips/Transcode/*")


if __name__ == "__main__":
    main()
