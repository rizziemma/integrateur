import happybase
import sys
import csv

conn = happybase.Connection(host='192.168.37.40', port=50001)

table = conn.table('data-plane')
b = table.batch()
print("connected to database")

name = sys.argv[1] + '-'
i = 0

with open(sys.argv[2]) as f :
	reader = csv.reader(f, delimiter='\t')
	for r in reader :
		if(i%100 == 0):
			print("push line " + str(i))
		#upload
		key = name + str(i)
		b.put(key, {b'date:date':r[0], b'hour:hour':r[1], b'manufacturer:manufacturer':r[2], b'operator:operator':r[3], b'model:model':r[4], b'planes:planes':r[5]})
		i = i + 1

print("sending batch")
b.send()
