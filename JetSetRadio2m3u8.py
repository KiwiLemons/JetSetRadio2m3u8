import argparse
import re
import os
import urllib.request
import sys

sources = ["butterflies","christmas","classic","crazytaxi","doomriders",
"elaquent","endofdays","future","ggs","goldenrhinos",
"halloween","hover","immortals","kingforanotherday","lofi",
"loveshockers","memoriesoftokyoto","noisetanks","ollieking","poisonjam",
"rapid99","revolution","summer","toejamandearl","ultraremixes"]
stationsDirectory = "radio/stations"

if sys.version_info < (3, 0):
    raise "This program requires Python version 3 or greater."

parser = argparse.ArgumentParser()
parser.add_argument("-m","--meaning",help="Displays the type of music that each m3u8 file contains",action="store_true")
parser.add_argument("-d","--destination", help="The dir where the m3u8 files are placed. If left blank it becomes the dir the program is running from.")
args = parser.parse_args()

if args.destination:
    dest = args.destination
else:
    dest = os.getcwd()
    for source in sources: 
        response = urllib.request.urlopen(f"https://jetsetradio.live/{stationsDirectory}/{source}/~list.js")  
        text = response.read().decode('utf-8')
        response.close()
        tracks = re.findall(r"] = \"([^\"]+)\"\;",text)
        try:
            newfile = open(f"{dest}\\{source}.m3u8","w")
        except FileNotFoundError as error:
            print(f"{dest} does not exist.")
            break
        else:
            newfile.write("#")
            for song in tracks:
                newfile.write(f"\nhttps://jetsetradio.live/{stationsDirectory}/{source}/{song}.mp3")
            newfile.close()
            print(f"Finished {source}")