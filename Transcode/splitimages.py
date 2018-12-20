import os
import io

imgdir = '/home/simon/Rips/Images/'

def parse_cue(cue_file):
    cf = io.open(cue_file, mode="r", encoding="ISO-8859-14")
    cue_lines = cf.readlines()
    for l in cue_lines:
        linestr = str(l)
        if linestr.startswith("FILE"):
            audio_filename = linestr[6:len(l)-7]
            return audio_filename

def main():
    for f in os.listdir(imgdir):
        if f.endswith(".cue"):
            cue_file = os.path.join(imgdir, f)
            audio_file = parse_cue(cue_file)
            print("Splitting CUE file: {}".format(cue_file))
            os.system("shnsplit -fq \"{}\" -o flac \"{}\"".format(cue_file, audio_file))

if __name__ == '__main__':
    main()
