# 2014.05.04 06:49:14 CEST
#Embedded file name: index.py
import json, sys
print 'Content-Type: text/txt\n'
q = sys.argv[-1]

def error(m):
    print m
    sys.exit()


if len(q) == 0:
    error('Input missing')
try:
    h, p = q.split(':')
except ValueError:
    error('Password missing')

try:
    i = json.load(open('../keys.json'))[h]
except:
    error('Invalid input')

print 'Right!' if p.isdigit() and len(p) < 15 and pow(i[0], int(p), i[1]) == i[2] else 'Wrong!\n' + '\n'.join(map(str, i))
+++ okay decompyling ../index.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2014.05.04 06:49:14 CEST
