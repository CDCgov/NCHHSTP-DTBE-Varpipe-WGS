#! /usr/bin/env python

""" Script accepts BEDTools coverage output file and samtools depth command output file   """
""" and estimates the coverage across genomic regions that are in the input file """

import sys

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
(start,end,gene_name,ids,length,perc_cov,temp_start) = ([],[],[],[],[],[],[])
idx = 0
sum_cov = 0.0
avg_cov = 0.0
fh1 = open(input1,'r')
for lines in fh1:
    fields = lines.rstrip("\r\n").split("\t")
    start.append(fields[1])
    end.append(fields[2])
    gene_name.append(fields[3])
    ids.append(fields[4])
    length.append(fields[8])
    perc_cov.append(fields[9])

fh1.close()

print "SAMPLE_ID" + "\t" + "CHROM" + "\t" + "START" + "\t" + "END" + "\t" + "GENE ID" + "\t" + "GENE NAME" + "\t" + "AVERAGE DEPTH" + "\t" + "PERCENT REGION COVERAGE"

new_start = start[idx]
new_end   = end[idx]

fh2 = open(input2,'r')
for lines in fh2:
    fields = lines.rstrip("\r\n").split("\t")
    if int(new_start) < int(fields[1]):
       sum_cov += float(fields[2])
       if int(fields[1]) == int(new_end) or int(fields[1]) > int(new_end):
         sum_cov -= float(fields[2])
         try:
            avg_cov = float("{0:.2f}".format(sum_cov/float(length[idx])))
         except ZeroDivisionError :
               pass
         avg_cov_str = str(avg_cov)
         covp = int(float(perc_cov[idx]) * 100)
         covp_str = str(covp)
         print input3 + "\t" + "NC_000962.3" + "\t" + new_start + "\t" + new_end + "\t" + gene_name[idx] + "\t" + ids[idx] + "\t" + avg_cov_str + "\t" + covp_str
         sum_cov = 0
         if idx < len(start) - 1:
            idx += 1
            new_start = start[idx]
            new_end   = end[idx]
    if int(fields[1]) > (int(end[-1]) - 1):
       sys.exit(1)

fh2.close() 

