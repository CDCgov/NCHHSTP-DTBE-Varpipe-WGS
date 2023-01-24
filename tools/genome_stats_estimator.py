#! /usr/bin/env python

import sys
from string import join

input1 = sys.argv[1]
input2 = sys.argv[2]

depth = 0
count = 0

fh1 = open(input1, 'r')
for lines in fh1:
    fields = lines.rstrip("\r\n").split("\t")
    depth += int(fields[2])
    if int(fields[2]) > 0:
       count += 1
fh1.close()
av_depth = depth/count
perc_cov = float((count/4411532.00)*100.00)
perc_cov_str = "{0:.2f}".format(perc_cov)
print "Sample ID" + "\t" +  "Average Genome Coverage Depth" + "\t" + "Percentage of Reference genome covered" + "\t" + "Pipeline Version"
print input2 + "\t" + str(av_depth) + "\t" +  perc_cov_str + "\t" + "Varpipe_wgs v1.0.1"

