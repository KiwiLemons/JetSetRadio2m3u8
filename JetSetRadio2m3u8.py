import argparse
import re
import os
from urllib import request, error
import sys

sources = ["butterflies","christmas","classic","crazytaxi","djchidow","doomriders","endofdays",
            "future","futuregeneration","ganjah","ggs","goldenrhinos","halloween","hover",
            "immortals","jetmashradio","lofi","loveshockers","noisetanks", "ollieking",
            "poisonjam","rapid99","revolution","siivagunner","summer","toejamandearl","ultraremixes"]
stationsDirectory = "radio/stations"

if sys.version_info < (3, 0):
    raise "This program requires Python version 3 or greater."

parser = argparse.ArgumentParser()
parser.add_argument("-d","--destination", help="The dir where the m3u8 files are placed. If left blank it becomes the dir the program is running from.")
args = parser.parse_args()

if args.destination:
    dest = args.destination
else:
    dest = os.getcwd()
    for source in sources: 
        req = request.Request(f"https://jetsetradio.live/{stationsDirectory}/{source}/~list.js")
        try:
            response = request.urlopen(req)
        except error.HTTPError as e:
            print(f"Skipped {source} ({e.code})")
        else:
            text = response.read().decode('utf-8')
            response.close()
            tracks = re.findall(r"] = \"([^\"]+)\"\;",text)
            try:
                newfile = open(f"{dest}\\{source}.m3u8","w")
            except FileNotFoundError:
                print(f"{dest} does not exist.")
                break
            else:
                newfile.write("#")
                for song in tracks:
                    newfile.write(f"\nhttps://jetsetradio.live/{stationsDirectory}/{source}/{song}.mp3")
                newfile.close()
                print(f"Finished {source}")