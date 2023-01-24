#! /usr/bin/env python

""" Aceepts target_coverage and genome coverage text files and sample name, generates stats output file """

import sys
import os
from string import join
from datetime import datetime

input1 = sys.argv[3]
input2 = sys.argv[4]
input3 = input2.split("-")[0]
input4 = sys.argv[5]
input5 = sys.argv[1]
input6 = sys.argv[2]

low_cov_count = 0

fh1 = open(input1)
for lines in fh1:  
  if lines.startswith("SAMPLE_ID"):
       continue
  lined = lines.rstrip("\r\n").split("\t")
  if lined[6] == "Review":
     low_cov_count += 1
fh1.close()

fh3 = open(input4)
for lines in fh3:
  if lines.startswith("SAMPLE_ID"):
       continue
  lined = lines.rstrip("\r\n").split("\t")
  genome_cov   =  lined[1] 
  genome_width =  lined[2] 
fh3.close()

fh5 = open(input5)
for lines in fh5:
    unmapped = int(lines.rstrip("\r\n"))
fh5.close()

fh6 = open(input6)
for lines in fh6:
    mapped = int(lines.rstrip("\r\n"))
fh6.close()

percent_mapped = (float(mapped)/float(unmapped))*100.00
str_percent_mapped = "{0:.2f}".format(percent_mapped)
i = datetime.now()

print "Sample ID" + "\t" + "Sample Name" + "\t" + "Percent Reads Mapped" + "\t" + "Average Genome Coverage Depth" + "\t" + "Percent Reference Genome Covered" + "\t" + "Coverage Drop" + "\t" + "Pipeline Version" + "\t" + "Date\r"
print input2 + "\t" + input3 + "\t" + str_percent_mapped + "\t" +  genome_cov + "\t" + genome_width + "\t" + str(low_cov_count) + "\t" + "Varpipeline: Varpipe_wgs_1.0.2" + "\t" + i.strftime('%Y/%m/%d %H:%M:%S') + "\r"

