# Usage: python exeggutor.py </path/to/binary>
import argparse, os

parser = argparse.ArgumentParser(description='Binary Deconstruction & Loader Script Wizard')
parser.add_argument('filename')
parser.add_argument('-v', dest='verbose',action='store_true',help='Verbose output')
args = parser.parse_args()
filey = args.filename
if filey[-1] == '/':
	print 'Invalid file name!'
	quit()
dump = [] # Dump bytes 
fraw = [] # Raw Bytes for calculation
hl = []   # Containing the unique bytes
il = []   # Index values of hl
sp = filey.split('/')
bn = sp[-1]  # Binary Name       
loady = bn + '_ldr.py'

def hxd():
    with open(filey, 'rb') as f:
        zCount = 0; # Counting Zeroes
        for chunk in iter(lambda: f.read(2), b''):
            # experimental
            fraw.append(chunk.encode('hex')) # Append to raw dump
            if chunk.encode('hex') == '0000':
                zCount = zCount + 1
                continue
            elif zCount > 0 and chunk.encode('hex') != '0000':
                dump.append('z' + str(zCount))
                zCount = 0
                dump.append(chunk.encode('hex'))
            else:
                dump.append(chunk.encode('hex'))
        f.close

def output():
    print "Sorted Hex Words \n    Length: " + hll + " items"
    if args.verbose:
        print '-'*79
        for item in hl:
            print item,
        print "\n"
    print "Indexed Values \n    Length: " + ill + " items"
    if args.verbose:
        print '-'*79
        for item in il:
            print item,
        print "\n"

hxd()

dll = str(len(fraw)*2) # Length of raw dump bytes

print """
 ______________   ____  __________ __________ _______________ _____ _________  _________  _________ 
/   /_____/\   \_/   / /   /_____//   /_____//   /_____/\   / \   //__     __\/    O    \|    _o___)
\___\XXXXX'/___/X\___\ \___\XXXXX'\___\XXXX.]\___\XXXX.]/___\_/___\`XX|___|XX'\_________/|___|\____\ 
 `BBBBBBBB'`BB'   `BB'  `BBBBBBBB' `BBBBBBBB' `BBBBBBBB'`BBBBBBBBB'    `B'     `BBBBBBB'  `BB' `BBB'
                                                                                           v0.171218"""

print "Original File: " + filey + "\n    Length: " + dll + " bytes"

hl = sorted(set(dump)) # Sorting the list of unique hex words
hll = str(len(hl))
# This creates the array from index values
for i in dump:
    if i in hl:
        pos = hl.index(i)
        il.append(pos)

ill = str(len(il))       # Length of index list
sb = len(il) + len(hl)   # Length of lists
sbs = str(sb)            # Converted to string
lessb = len(fraw)*2 - sb # Amount of space saved
lbs = str(lessb)         

output()

print "\nRepresenting " + dll + " bytes with " + sbs + " bytes for a total savings of [" + lbs + "] bytes!"

# Begins writing the *_ldr.py file
#os.chdir("/tmp/")
with open(loady, "a") as lo:
    lo.write('import binascii\nimport subprocess\n')
    lo.write('\n# Sorted hex words: ' + hll + ' items\n')
    lo.write('\nhl = ')
    lo.write(str(hl))
    lo.write('\n\n# Indexed Values: ' + ill + ' items\n')
    lo.write('\nil = ')
    lo.write(str(il))
    lo.write('\n\nm = "' + bn + '_clone"')
    lo.write('\nwith open(m, \'wb\') as f:') 
    lo.write('\n\tfor i in il:')
    lo.write('\n\t\tif hl[i][0] == \'z\':')
    lo.write('\n\t\t\tzx = hl[i][1:]')
    lo.write('\n\t\t\tzl = \'0\'*int(zx)*4')
    lo.write('\n\t\t\tww = binascii.a2b_hex(\'\'.join(zl))')
    lo.write('\n\t\t\tf.write(ww)')
    lo.write('\n\t\telse:')
    lo.write('\n\t\t\tww = binascii.a2b_hex(\'\'.join(hl[i]))')
    lo.write('\n\t\t\tf.write(ww)')
    lo.write("\nsubprocess.Popen(['/bin/chmod','+x','" + bn + "_clone'])")

fsz = os.path.getsize(loady) 
print "\n[^0^] A " + str(fsz) + " byte loader script was generated! exec --> 'python " + loady + "'"
