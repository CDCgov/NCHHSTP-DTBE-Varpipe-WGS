#!/usr/bin/env python

import sys
import re
from string import join

""" The script accepts the genome loci coverage report the per position coverage report and a BED file """
""" it outputs a report of the presence and propeties of structural variants in positions in the BED file """

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
input4 = sys.argv[4]

(genename,strand,start,stop,posarray,newlinne)            = ([],[],[],[],[],[])
(cdsstart,cdsend,startpos,stoppos,pstoppos,pstartpos,svlength,delstart,delend,gene,strandor) = (0,0,0,0,0,0,0,0,0,"","")
(aastart,aaend) = ("","")
evalu = False

fh1 = open(input1,'r')
for lines in fh1:
    if lines.startswith("#"):
       continue
    fields = lines.rstrip("\r\n").split("\t")
    genename.append(fields[3])
    strand.append(fields[5])
    start.append(fields[1])
    stop.append(fields[2])
fh1.close()

fh3 = open(input3,'r')
for lines in fh3:
    fields = lines.rstrip("\r\n").split("\t")
    if fields[1] in start:
       evalu     = True
       startpos  = int(fields[1])
       ind       = start.index(fields[1])
       stoppos   = int(stop[ind])
       if ind != 0:
          pstoppos  = int(stop[ind -1 ])
          pstartpos = int(start[ind -1])
       gene      = genename[ind]
       strandor  = strand[ind]
    if int(fields[2]) == 0 and evalu == True:
       posarray.append(fields[1])
    if fields[1]  == str(stoppos) and evalu == True:
       evalu      = False
       if len(posarray) > 1:
          delstart   = int(posarray[0])
          delend     = int(posarray[len(posarray) - 1])
          svlength   = delend - delstart
       if strandor == "forward":
          cdsstart =  (delstart + 1) - startpos
          cdsend   =  (delend + 1) - startpos
          aastart1  = "{0:.1f}".format(cdsstart/3)
          aaend1    = "{0:.1f}".format(cdsend/3)
          if aastart1[-1] == '0' and aastart1[0] != '0':
             aastart = aastart1[:-2]
          else:
             aastart = str(int(aastart1[:-2]) + 1)
          if aaend1[-1] == '0' and aaend1[0] != '0' :
             aaend = aaend1[:-2]
          else:
             aaend = str(int(aaend1[:-2]) + 1)
       elif strandor == "reverse":
          cdsstart = (stoppos + 1) - delend
          cdsend   = (stoppos + 1) - delstart
          aastart1  = "{0:.1f}".format(cdsstart/3)
          aaend1    = "{0:.1f}".format(cdsend/3)
          if aastart1[-1] == '0' and aastart1[0] != '0':
              aastart = aastart1[:-2]
          else:
              aastart = str(int(aastart1[:-2]) + 1)
          if aaend1[-1] == '0' and aaend1[0] != '0':
             aaend = aaend1[:-2]
          else:
             aaend = str(int(aaend1[:-2]) + 1)
       elif strandor == "reverse_promoter":
          cdsstart = (pstoppos ) - delstart
          cdsend   = (pstoppos ) - delend
          aastart  = "NA"
          aaend    = "NA"
       elif strandor == "forward_promoter":
          cdsstart =  delend - pstartpos
          cdsend   =  delstart - pstartpos
          aastart  = "NA"
          aaend    = "NA"
       else:
          cdsstart = 0
          cdsend   = 0
          
       if len(posarray) < 10:
          continue
       if len(posarray) > 1:
          printline = input4 + "\t" + gene + "\t" + str(svlength) + "\t" + str(delstart) + "\t" + str(delend) + "\t" + str(cdsstart) + "\t" + str(cdsend) + "\t" + aastart + "\t" + aaend
          if (stoppos - startpos) > svlength:
             newlinne.append(printline)
       posarray = []
fh3.close()

print "Sample ID" + "\t" + "Gene" + "\t" + "SV Length" + "\t" + "Ref_Start" + "\t" + "Ref_Stop" + "\t" + "CDS_start" + "\t" + "CDS_stop" + "\t" + "Amino Acid_start" + "\t" + "Amino_acid_end"
    
fh2 = open(input2,'r')
for lines in fh2:
    if lines.startswith("SAMPLE_ID"):
       continue
    fields = lines.rstrip("\r\n").split("\t")
    if fields[5] in genename:
       if float(fields[6]) > 2.0 and int(fields[7]) > 99:
          print input4 + "\t" + fields[5] + "\t" + "NA" + "\t" +  "No large deletion" + "\t" + "No large deletion" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA"
       elif float(fields[6]) < 2.0 or int(fields[7]) < 1:
          print input4 + "\t" + fields[5] + "\t" + "NA" + "\t" + "Complete deletion" + "\t" + "Complete deletion" +  "\t" + "NA" + "\t" + "NA" + "\t" + "NA" + "\t" + "NA"
       else:
          for x in newlinne:
              print x
          newlinne = []

