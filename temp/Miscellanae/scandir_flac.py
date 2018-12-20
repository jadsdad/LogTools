from mutagen import oggvorbis
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
basedir = sys.argv[1]
out = open(dir_path + "/output.tab","w")
lines = []

for f in os.listdir(basedir):
    if f.endswith(".ogg"):
        print("Scanning : " + f)
        file = os.path.join(basedir, f)
        f = oggvorbis.OggVorbis(file)
        t = f.tags

        line = [t["ALBUMARTIST"][0],
                t["Album"][0],
                str(t["Date"][0]),
                str(t["DISCNUMBER"][0]),
                str(t["tracknumber"][0]),
                t["Artist"][0],
                t["title"][0],
                str(int(f.info.length))]

        text_line = "\t".join(line)
        lines.append(text_line + "\n")

out.writelines(lines)
out.flush()
out.close()

