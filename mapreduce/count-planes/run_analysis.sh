#!/bin/bash
#./run_analysis.sh lzip_dir aircraft_db mapper reducer
source ~/.bashrc

#preparing pcap dir
rm -rf /data2/$1
mkdir /data2/$1
echo "copying zip files"
cp -r /data/$1 /data2/

echo "extracting files"
lzip -d /data2/$1/*

#making csv files
rm -rf /data2/out$1
mkdir /data2/out$1

#echo "map to csv"
python map_to_csv.py /data2/$1/ /data2/out$1/ $2

#cleaning up unzip files
echo "deleting extracted files"
rm -rf /data2/$1

#hadoop
echo "upload to hdfs"
hadoop fs -rm -r -skipTrash in$1
hadoop fs -mkdir in$1
hadoop fs -put /data2/out$1/* in$1

echo "running mapreduce"
mapreduce $3 $4 in$1 out$1

#uploading results to hbase
echo "downloading results"
rm /data2/results$1
hadoop fs -get out$1/part-00000 /data2/results$1
python results_to_hbase.py $1 /data2/results$1

hadoop fs -rm -r -skipTrash in$1
hadoop fs -rm -r -skipTrash out$1
rm -rf /data2/out$1/

#print end time
date
