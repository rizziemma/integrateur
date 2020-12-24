#!/usr/bin/python

import sys
import csv

writer = csv.writer(sys.stdout, delimiter='\t')

planes = 0

oldPlane = None
oldKeys = None

for line in sys.stdin :
	data = line.strip().split('\t')
	if len(data) != 6:
		continue
	thisKeys = data[0:5]
	thisPlane = data[5]
#	print(thisKeys)
#	print(thisPlane)

	if oldKeys and oldKeys != thisKeys :
		writer.writerow(oldKeys + [planes])
		planes = 0

	oldKeys = thisKeys
	if thisPlane != oldPlane :
		planes += 1

	oldPlane = thisPlane

if oldKeys != None:
	writer.writerow(oldKeys + [planes])

