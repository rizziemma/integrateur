import asterix
import dpkt
import sys
import csv
import os


input_dir = sys.argv[1]
output_dir = sys.argv[2]
database_plane = sys.argv[3]

planes = {}

print("parsing planes data base")
with open(database_plane) as f :
	reader = csv.reader(f)
	for line in reader :
		p = line[0]
		man = line[3] if line[3] != "" else False
		mod = line[4] if line[4] != "" else False
		ope = line[9] if line[9] != "" else False
		planes[p] = {'manufacturer':man, 'model':mod, 'operator':ope}

print("starting file to csv")
for filename in os.listdir(input_dir) :
	print("to csv : " + filename)

	name = filename.split('.pcap')[0]
	date = name[0:10]

	with open(input_dir+filename) as in_file :
		with open(output_dir+name+'.csv', 'w') as out_file :
			writer = csv.writer(out_file, delimiter='\t')
			pcap = dpkt.pcap.Reader(in_file)

			cntr=1
			for ts, buf in pcap:
				eth = dpkt.ethernet.Ethernet(buf)
				data = eth.ip.udp.data

				cntr += 1

				# Parse data
				parsed = asterix.parse(data)

				time = False

				for packet in parsed :
					plane = [False for i in range(6)]
					addr = False
					if 'I220' in packet :
						if 'ACAddr' in packet['I220']:
							if 'val' in packet['I220']['ACAddr']:
								addr = str(packet['I220']['ACAddr']['val'])

					for time_label in ['I030', 'I140'] :
						if time_label in packet :
							if 'ToD' in packet[time_label] :
								if 'val' in packet[time_label]['ToD'] :
									time = float(packet[time_label]['ToD']['val'])
									time = int(time / 3600) #seconds to hours
									break
					if date and addr :
						if addr in planes :
							line = planes[addr]
							plane = [date, time, line['manufacturer'], line['operator'], line['model'], addr]
						else :
							plane = [date, time, False, False, False, addr]
						writer.writerow(plane)
