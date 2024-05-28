import argparse
import requests
import re

parser = argparse.ArgumentParser(description='Create a m3u playlist from a phishtracks page based on the date')
parser.add_argument('date')
args = parser.parse_args()

r=requests.get('https://www.phishtracks.com/shows/'+args.date)

mp3regex=r"//assets.phishtracks.com(?:[a-zA-Z0-9_./])+mp3\?[0-9]*"
mp3list=re.findall(mp3regex,r.text)

nameregex = r'title\"\:\"(?:[a-zA-Z0-9 \'.\-&#;\:\>\\\,])*\",\"position'
names=re.findall(nameregex,r.text)

print('#EXTM3U')
print('#PLAYLIST:Phish '+args.date)
print('#EXTART:Phish')
for n in range(len(mp3list)):
    print('#EXTINF:-1,'+names[n][8:-11].replace('\\u003e','>'))
    print('https:' + mp3list[n])
