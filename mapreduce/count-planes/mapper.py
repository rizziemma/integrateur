#!/usr/bin/python
import sys
import os

try:
	import asterix
	import dpkt
except ImportError:
	#zipdir = "env-mapreduce.zip"
	libdir = 'env-mapreduce.zip/lib/python2.7/site-packages'

	#zipdir_exists = os.path.exists(zipdir)
	#if zipdir_exists :
	#	import zipfile
	#	with zipfile.ZipFile(zipdir, 'r') as zip_ref:
	#		zip_ref.extractall(libdir)

	if os.path.exists(libdir):
		if os.path.isdir(libdir) and libdir not in sys.path:
			sys.path.insert(0, libdir)

	else:
		raise ImportError("env dir (%s) doesn't exists" % libdir)

	import asterix
        import dpkt

	read_input = False
	infile = sys.stdin

	while(not read_input and not(infile is  None)) :
		try :
			pcap = dpkt.pcap.Reader(infile)
			read_input = True
		except Exception:
			if infile.readline() is None :
				infile = None

	cntr=1
	if read_input :
		try :
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
					#print(e)
					continue
		except Exception as e :
			pass
