import asterix
import dpkt

# Read example file from packet resources
#sample_filename = 'extrait.pcap'
sample_filename = '2020-09-04-2225.pcap'
categories = {}
planes = {}
planes_number = 0
with open(sample_filename) as f:
	pcap = dpkt.pcap.Reader(f)

	cntr=1
	for ts, buf in pcap:
		eth = dpkt.ethernet.Ethernet(buf)
		data = eth.ip.udp.data

		#hexdata = ":".join("{:02x}".format(ord(c)) for c in str(data))
		#print('Parsing packet %d : %s' %(cntr, hexdata))
		cntr += 1

		# Parse data
		parsed = asterix.parse(data)
		for packet in parsed :
			plane = False
			if 'I240' in packet :
				if 'TId' in packet['I240']:
					if 'val' in packet['I240']['TId']:
						plane = str(packet['I240']['TId']['val'])
			cat = str(packet['category'])
			if cat in categories :
				categories[cat] = categories[cat] + 1
			else :
				categories[cat] = 1
			if plane :
				planes_number = planes_number + 1
				if plane in planes:
					planes[plane] = planes[plane] + 1
				else :
					planes[plane] = 1
print("PLANES :")
print(planes)
print("SUM PLANES :")
print(planes_number)
print("CATEGORIES :")
print(categories)

        
