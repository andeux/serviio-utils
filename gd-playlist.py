import argparse
import requests
import re

parser = argparse.ArgumentParser(description='Create a playlist from an archive link')
parser.add_argument('show')
args = parser.parse_args()

r=requests.get(args.show)

nameregex=r"name\" content=\"(?:[a-zA-Z0-9 \'\&\.\->,+\(\)\:\!])*"
namelist=re.findall(nameregex,r.text)

mp3regex=r"associatedMedia\" href=\"https://archive.org/download/(?:[a-zA-Z0-9\-\./ %>_])*.mp3"
mp3list=re.findall(mp3regex,r.text)

print('#EXTM3U')
for x in range(len(mp3list)):
    print('#EXTINF:-1,'+namelist[x+1][15:])
    print(mp3list[x][23:])
