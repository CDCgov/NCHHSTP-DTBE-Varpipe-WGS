#! /usr/bin/env python

""" Script reads samtools depth command output file   """
""" and checks for drops in coverage across positions in the input file """

import sys

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
(start,end,gene_name,gene_id,temp_start) = ([],[],[],[],[])
idx = 0
flag    = "No deletion"
fh1 = open(input1,'r')
for lines in fh1:
    fields = lines.rstrip("\r\n").split("\t")
    start.append(fields[1])
    end.append(fields[2])
    gene_name.append(fields[4])
    gene_id.append(fields[3])

fh1.close()

print "SAMPLE_ID" + "\t" + "CHROM" + "\t" + "Start" + "\t" + "End" + "\t" + "Gene Name" + "\t" + "Gene ID" + "\t" + "Flag\r"

new_start = start[idx]
new_end   = end[idx]

fh2 = open(input2,'r')
for lines in fh2:
    fields = lines.rstrip("\r\n").split("\t")
    if int(new_start) < int(fields[1]):
      if int(fields[2]) < 10:
         flag = "Review"
      if int(fields[1]) == int(new_end) or int(fields[1]) > int(new_end):
         print input3 + "\t" + "NC_000962.3" + "\t" + new_start + "\t" + new_end + "\t" + gene_name[idx] + "\t" + gene_id[idx] + "\t" + flag + "\r"
         flag   = "No deletion"
         if idx < len(start) - 1:
            idx += 1
            new_start = start[idx]
            new_end   = end[idx]
    if int(fields[1]) > (int(end[-1]) - 1):
       sys.exit(1)
fh2.close() 

