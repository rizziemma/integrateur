#!/usr/bin/python

import asterix
import dpkt
import sys


planes = 0

oldTime = None
oldPlane = None

for line in sys.stdin :
	data = line.strip().split('\t')
	if len(data) != 2:
		continue
	
	thisTime, thisPlane = data
	
	if oldTime and oldTime != thisTime :
		print('{0}\t{1}'.format(oldTime, planes))
		planes = 0
			
	oldTime = thisTime
	if thisPlane != oldPlane :
		planes += 1
	
	oldPlane = thisPlane

if oldTime != None:
	print('{0}\t{1}'.format(oldTime, planes))
	

        
