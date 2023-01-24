#!/usr/bin/bash

if [ -n '*_L001_R2_001*' ]
then

   ls *_L001_R2_001* | sed 's/_L001_R2_001.fastq.gz//g' | awk '{print "cat "$0"_L001_R2_001.fastq.gz "$0"_L002_R2_001.fastq.gz "$0"_L003_R2_001.fastq.gz "$0"_L004_R2_001.fastq.gz >> "$0"_R2_001.fastq.gz"}' > run_2.sh

fi

if [ -n '*_L001_R2_001*' ]
then

    ls *_L001_R1_001* | sed 's/_L001_R1_001.fastq.gz//g' | awk '{print "cat "$0"_L001_R1_001.fastq.gz "$0"_L002_R1_001.fastq.gz "$0"_L003_R1_001.fastq.gz "$0"_L004_R1_001.fastq.gz >> "$0"_R1_001.fastq.gz"}' > run_1.sh

fi

if [ -e run_1.sh ]
then

   sh run_1.sh

fi

if [ -e run_2.sh ]
then

   sh run_2.sh

fi

if [ -n '*_L001_R1*' ]
then

   rm *_L00*

fi

ls *_R1_001.fastq.gz | sed 's/_R1_001.fastq.gz//g' | awk '{print "../tools/Varpipeline -q "$0"_R1_001.fastq.gz -r ../tools/ref2.fa -n "$0" -q2 "$0"_R2_001.fastq.gz -a -v"}' > run_3.sh


sh run_3.sh
rm *.fastq.gz
rm run_3.sh

if [ -e run_1.sh ]
then

   rm run_1.sh   

fi

if [ -e run_2.sh ]
then

   rm run_2.sh

fi

