import argparse
import re
import sys
import os
import requests

sources = ["https://jetsetradio.live/audioplayer/stations/classic/~list.js",
"https://jetsetradio.live/audioplayer/stations/doomriders/~list.js",
"https://jetsetradio.live/audioplayer/stations/future/~list.js",
"https://jetsetradio.live/audioplayer/stations/ggs/~list.js",
"https://jetsetradio.live/audioplayer/stations/goldenrhinos/~list.js",
"https://jetsetradio.live/audioplayer/stations/immortals/~list.js",
"https://jetsetradio.live/audioplayer/stations/loveshockers/~list.js",
"https://jetsetradio.live/audioplayer/stations/noisetanks/~list.js",
"https://jetsetradio.live/audioplayer/stations/poisonjam/~list.js",
"https://jetsetradio.live/audioplayer/stations/rapid99/~list.js",
"https://jetsetradio.live/audioplayer/stations/summer/~list.js"]

parser = argparse.ArgumentParser()
parser.add_argument("-m","--meaning",help="Displays the type of music that each m3u8 file contains",action="store_true")
parser.add_argument("-d","--destination", help="The dir where the m3u8 files are placed. If left blank it becomes the dir the program is running from.")
args = parser.parse_args()
if args.meaning:
     print("CLASSIC - Plays the Original Jet Set Radio Soundtrack!\nFUTURE - Plays the Jet Set Radio Future Soundtrack!\nGG's - Funky energetic beats with positive vibes!\nPOISON JAM - Grunge rock & metal with that monster sound!\nNOISE TANKS - Digital & electronic sounds to fry your brain!\nLOVE SHOCKERS - Twisted, heartbroken, & love-sick ladies!\nRAPID 99 - Upbeat & chill female tunes!\nTHE IMMORTALS - Ethnic music & balkan beats!\nDOOM RIDERS - Biker music & classic rock!\nGOLDEN RHINOS - Hip-Hop beats with deep classical rhythms of power and authority!")
else:
     if args.destination:
         dest = args.destination
     else:
         dest = os.getcwd()
     for source in sources:
         #add except for no internet connection
         response = requests.get(source).text
         #findall returns a list with tuples in each element for groups
         matches = re.findall(r"(.+)Array\[\1Array\.length\] = \"([^\"]+)\"\;",response)
         #test if this is faster
         station = matches[0][0].lower()
         try:
             newfile = open(f"{dest}\\{station.capitalize()}.m3u8","w")
         except FileNotFoundError as error:
             #Currently if a destination is not valid then you have to go through the entire process of evaluating a whole source before it is noticed.
             print(f"{dest} does not exist.")
             break
         else:
             newfile.write("#")
             for idx, song in enumerate(matches):
                 newfile.write(f"\nhttps://jetsetradio.live/audioplayer/stations/{station}/{matches[idx][1]}.mp3")
             newfile.close()
             print(f"Finished {station.capitalize()}")