#!/usr/bin/python

import asterix
import dpkt
import sys


try :
	pcap = dpkt.pcap.Reader(sys.stdin)
	cntr=1
	for ts, buf in pcap:
		try :
			eth = dpkt.ethernet.Ethernet(buf)
			data = eth.ip.udp.data
			cntr += 1
			parsed = asterix.parse(data)
			time = False

			for packet in parsed :
				plane = False

				if 'I220' in packet :
					if 'ACAddr' in packet['I220']:
						if 'val' in packet['I220']['ACAddr']:
							plane = str(packet['I220']['ACAddr']['val'])

				for time_label in ['I030', 'I140'] :
					if time_label in packet :
						if 'ToD' in packet[time_label] :
							if 'val' in packet[time_label]['ToD'] :
								time = float(packet[time_label]['ToD']['val'])
								time = int(time / 3600) #seconds to hours
								break

				if time and plane :
					print('{0}\t{1}'.format(time, plane))
		except Exception as e :
			#pass
			print(e)
			continue
except Exception as e :
	print(e)
