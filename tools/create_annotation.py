#! /usr/bin/env python

import sys



""" The script accepts a SnpEff annotated VCF file and the sample ID name (string) as input options """
""" it parses files and creates a final annotation file """


input1 = sys.argv[1]
input2 = sys.argv[2]

position            = ""
reference           = ""
alternate           = ""
filterr             = ""
GT		    = ""
AD                  = ""
AF                  = ""
DP                  = ""
F1R2                = ""
F2R1                = ""
FAD                 = ""
PGT                 = ""
PID                 = ""
PS                  = ""
SB                  = ""
AS_FilterStatus     = ""
AS_SB_TABLE         = ""
rDP                 = ""
ECNT                = ""
MBQ                 = ""
MFRL                = ""
MMQ                 = ""
MPOS                = ""
POPAF               = ""
RPA                 = ""
RU                  = ""
TLOD                = ""
ANN                 = ""


fh1 = open(input1,'r')

print "Sample ID" + "\t" + "CHROM" + "\t" + "POS" + "\t" + "REF" + "\t" + "ALT" + "\t" + "FILTER" + "\t" + "GT" + "\t" +  "AD" + "\t" + "AF" + "\t" + "DP" + "\t" + "F1R2 " + "\t" + "F2R1" + "\t" + "FAD" + "\t" + "PGT" + "\t" + "PID" + "\t" + "PS" + "\t" "SB" + "\t" + "AS_FilterStatus" + "\t" + "AS_SB_TABLE" + "\t" + "rawDP" + "\t" + "ECNT" + "\t" + "MBQ" + "\t" + "MFRL" + "\t" + "MMQ" + "\t" + "MPOS" + "\t" + "POPAF" + "\t" + "RPA" + "\t" + "RU" + "\t" + "TLOD" + "\t" + "ANN\r"  

for lines in fh1:
    if lines.startswith("#"):
       continue
    fields    = lines.rstrip("\r\n").split("\t")
    position  = fields[1]
    reference = fields[3]
    alternate = fields[4]
    filterr   = fields[6]
    rarr      = fields[9].split(":")
    GT        = rarr[0]
    AD        = rarr[1]
    AF        = rarr[2]
    DP        = rarr[3]
    F1R2      = rarr[4]
    F2R1      = rarr[5]
    FAD       = rarr[6]
    if len(rarr) == 8:
       SB     = rarr[7]
    else:
       PGT       = rarr[7]
       PID       = rarr[8]
       PS        = rarr[9]
       SB        = rarr[10]
    infoarr   = fields[7].split(";")
    for x in infoarr:
        if "AS_FilterStatus" in x:
            AS_FilterStatus   = x.split("=")[1]
        if "DP" in x:
            rDP     = x.split("=")[1]
        if "ECNT" in x:
            ECNT    = x.split("=")[1]
        if "MBQ" in x:
            MBQ     = x.split("=")[1]
        if "MFRL" in x:
            MFRL    = x.split("=")[1]
	if "MMQ" in x:
            MMQ     = x.split("=")[1]
 	if "MPOS" in x:
            MPOS    = x.split("=")[1]
	if "POPAF" in x:
            POPAF   = x.split("=")[1]    
	if "AS_SB_TABLE" in x:    
       	    AS_SB_TABLE    = x.split("=")[1]
	if "TLOD" in x:
            TLOD    = x.split("=")[1]
        if "ANN" in x:
            ANN     = x
	if "RPA" in x:
            RPA     = x.split("=")[1]
	if "RU" in x:
       	    RU      = x.split("=")[1]
    print input2 + "\t" + fields[0] + "\t" + position + "\t" + reference + "\t" + alternate + "\t" + filterr + "\t" + GT + "\t" + AD + "\t" + AF + "\t" + DP + "\t" + F1R2 + "\t" + F2R1 + "\t" + FAD + "\t" + PGT + "\t" + PID + "\t" + PS + "\t" + SB + "\t" + AS_FilterStatus + "\t" + AS_SB_TABLE + "\t" + rDP + "\t" + ECNT + "\t"+ MBQ + "\t" + MFRL + "\t" + MMQ + "\t" + MPOS + "\t" + POPAF + "\t" + RPA + "\t" + RU + "\t" + TLOD + "\t" + ANN + "\r" 
    (PGT,PID,PS,RPA,RU) = ("","","","","")
fh1.close()
