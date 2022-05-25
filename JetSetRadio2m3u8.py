import argparse
from ast import excepthandler
import re
import os
from urllib import request, error
import sys

sources = ["bumps", "butterflies","christmas","classic","crazytaxi","djchidow","doomriders","endofdays",
            "future","futuregeneration","ganjah","ggs","goldenrhinos","halloween","hover",
            "immortals","jetmashradio","lofi","loveshockers","noisetanks", "ollieking",
            "poisonjam","rapid99","revolution","siivagunner","summer","toejamandearl","ultraremixes"]
stationsDirectory = "radio/stations"

if sys.version_info < (3, 0):
    raise "This program requires Python version 3 or greater."

parser = argparse.ArgumentParser()
parser.add_argument("-d","--destination", help="The dir where the m3u8 files are placed. If left blank it becomes the dir the program is running from.")
parser.add_argument("-b", "--bumps", action=argparse.BooleanOptionalAction, help="Includes the bumps station", default=False)
parser.add_argument("--update", action=argparse.BooleanOptionalAction, default=True, help="Downloads newest stations on JetSetRadio, uses old backup stations with --no-update")
args = parser.parse_args()

def UpdateStations():
    try:
        response = request.urlopen("https://www.jetsetradio.live")
    except:
        print("Error, Prorbably should not continue with program if this request fails")
    else:
        text = response.read().decode()
        stations = re.findall(r"<script src=\"radio\/stations\/(.+?)\/~list\.js\"><\/script>", text)
        if len(stations):
            global sources
            sources = stations
            print("Updated stations")
        else:
            print("Failed to find new stations, using backup")

if args.update: 
    UpdateStations()

if not args.bumps:
    try:
        sources.remove("bumps")
    except ValueError:
        pass

if args.destination:
    dest = args.destination
else:
    dest = os.getcwd()

failed = 0
for source in sources: 
    req = request.Request(f"https://jetsetradio.live/{stationsDirectory}/{source}/~list.js")
    try:
        response = request.urlopen(req)
    except error.HTTPError as e:
        failed += 1
        print(f"Skipped {source} ({e.code})")
    else:
        text = response.read().decode('utf-8')
        response.close()
        tracks = re.findall(r"] = \"([^\"]+)\"\;",text)
        try:
            newfile = open(f"{dest}\\{source}.m3u8","w", encoding="utf-8")
        except FileNotFoundError:
            print(f"{dest} does not exist.")
            break
        else:
            newfile.write("#EXTM3U")
            for song in tracks:
                newfile.write(f"\n#EXTINF:-1,{song}")
                newfile.write(f"\nhttps://jetsetradio.live/{stationsDirectory}/{source}/{song}.mp3")
            newfile.close()
            print(f"Finished {source}")
print(f"Saved {len(sources) - failed} stations to {dest}")