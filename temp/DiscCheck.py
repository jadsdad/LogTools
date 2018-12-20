import os
from mutagen import oggvorbis

basedir = "\home\simon\Music"

for root, dirs, files in os.walk(basedir):
    for f in files:
        if f.endswith(".ogg"):
            # print("Scanning : " + f)
            file = os.path.join(root, f)
            try:
                f = oggvorbis.OggVorbis(file)
                d = f["DISCNUMBER"][0]
            except oggvorbis.OggVorbisHeaderError:
                print ("-- Error in file header " + file)
            except KeyError:
                f['DISCNUMBER'] = ['1']
                f.save()
                print ("Written Disc No to " + file)
