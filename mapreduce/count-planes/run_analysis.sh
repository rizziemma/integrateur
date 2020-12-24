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
rm -rf /data2/out
mkdir /data2/out

echo "map to csv"
python map_to_csv.py /data2/$1/ /data2/out/ $2

#cleaning up unzip files
echo "deleting extracted files"
rm -rf /data2/$1

#hadoop
echo "upload to hdfs"
hadoop fs -rm -r -skipTrash in
hadoop fs -mkdir in
hadoop fs -put /data2/out/* in

echo "running mapreduce"
mapreduce $3 $4 in out

#uploading results to hbase
echo "downloading results"
rm /data2/results
hadoop fs -get out/part-00000 /data2/results
python results_to_hbase.py /data2/results

