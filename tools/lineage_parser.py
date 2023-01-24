#! /usr/bin/env python

""" This script accepts the final annotation file and the lineage marker SNPs file  """
""" and infers the lineage and possible sublineage classification of the isolate  """
""" it requires a sample ID name (string) and an output file name(string) """

import sys
from string import join

input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]
input4 = sys.argv[4]

fh1 = open(input1, 'r')
sublinn = ""
(lineage,position,ref,alt) = ([],[],[],[])
prevlin = []
prevsub = []
tribes = ["lineages","Indo-Oceanic","East-Asian","East-African-Indian","Euro-American","West-Africa 1","West-Africa 2","Ethiopian"]
(concord,discord,concord1,discord1,count) = (0,0,0,0,0)
discordance = False
sublinneage = False
animals     = False
linfour = ""
hrv37 = ""
CAP = ""
BCG = ""   
BOV = ""
ORYX = ""

for lines in fh1:
    if lines.startswith('#'):
       continue
    fields = lines.rstrip("\r\n").split("\t")
    lineage.append(fields[0])
    position.append(fields[1])
    ref.append(fields[2])
    alt.append(fields[3])
fh1.close()

fh2 = open(input2,'r')
for lines in fh2:
    count += 1
    fields = lines.rstrip("\r\n").split("\t")
    if fields[2] == '931123':
       linfour = fields[2]
    if fields[2] == '1759252':
       hrv37 = fields[2]
    if fields[2] == '2831482':
       CAP = fields[2]
       animals = True
       print "SNP" + " " + fields[2] + " " + "suggests M. caprae " 
    if fields[2] == '2289073':
       BOV = fields[2]
       animals = True
       print "SNP" + " " + fields[2] + " " + "suggests M. bovis "
    if fields[2] == '8624':
       BCG = fields[2]
       animals = True
       print "SNP" + " " + fields[2] + " " + "suggests M. bovis-BCG "
    if fields[2] == '2726378':
       ORYX = fields[2]
       animals = True
       print "SNP" + " " + fields[2] + " " + "suggests M. orygis "
    if fields[2] in position:
       ind = position.index(fields[2])
       if alt[ind] == fields[4]:
          if len(lineage[ind]) > 1:
             sublin = lineage[ind]
             prevsub.append(sublin)
             sublinn = prevsub[0]
             print "SNP" + " " + position[ind] + " " + "suggests sub-lineage: " + lineage[ind]
             for i in range(0,len(prevsub)):
                 if len(sublinn) < len(prevsub[i]) : 
                    sublinn = prevsub[i]     
          else:
                lin = lineage[ind]
                prevlin.append(lin)
                print "SNP" + " " + position[ind] + " " + "suggests lineage: " + lineage[ind]
fh2.close()

fh3 = open(input3,'w')
print >> fh3, "Sample ID" + "\t" + "Lineage" + "\t" + "Lineage Name" 

split_first = ['NA']
if len(prevsub) > 0:
   split_first = sublinn.split(".")
   sublinneage = True
if len(prevlin) == 0:
      for i in range(0,len(prevsub)): 
          split_lin = prevsub[i].split(".")
          if split_lin[0] != split_first[0]:
             discordance = True
          if split_lin[1] != split_first[1]:
             discordance = True
      if discordance:
         print "no precise lineage inferred"
         print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)"
         sys.exit(1)
      else:
         if len(split_first) > 1 and animals == False :
            print "Lineage: " + split_first[0] + " :  " + tribes[int(split_first[0])]
            print >> fh3, input4 + "\t" + split_first[0] + "\t" + tribes[int(split_first[0])]
         elif len(split_first) > 1 and animals == True :
            print "no precise lineage inferred"
            print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)"
            sys.exit(1)
         elif len(linfour) < 2 and animals == False:
            print "Absence of SNP 931123 suggests lineage 4"
            print "Lineage: " + "4" + " :  " + "Euro-American"
            if len(hrv37) > 2:
               print >> fh3, input4 + "\t" + "4" + "\t" + "Euro American"
            elif len(hrv37) < 2:
               print "Absence of SNP 1759252 suggests sublineage 4.9"
               print >> fh3, input4 + "\t" + "4" + "\t" + "Euro American"
         elif len(linfour) < 2 and animals == True:
            print "no precise lineage inferred"
            print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)"
            sys.exit(1)
         elif len(BCG) > 0:
            print "Lineage: " + "Bovis-BCG"
            print >> fh3, input4 + "\t" + "Bovis-BCG" + "\t" + "M.bovis-BCG"
         elif len(BOV) > 0:
            print "Lineage: " + "Bovis"
            print >> fh3, input4 + "\t" + "Bovis" + "\t" + "M.bovis"
         elif len(ORYX) > 0:
            print "Lineage: " + "Oryx"
            print >> fh3, input4 + "\t" + "Oryx" + "\t" + "M.orygis"
         elif len(CAP) > 0:
            print "Lineage: " + "Caprae"
            print >> fh3, input4 + "\t" + "Caprae" + "\t" + "M.caprae"
         else:
            print "No Informative SNPs detected"
            print >> fh3, input4 + "\t" + "No Informative SNPs detected" + "\t" + "No Informative SNPs detected"
else:
      if len(prevlin) > 1:
        for j in range(0,len(prevlin)): 
            if prevlin[0] != prevlin[j]:
               discordance = True
        if discordance == True:
           print "no concordance between predicted lineage and sublineage(s)"
           print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)" + "\t" + "NA"
           sys.exit(1) 
      else:
        if len(sublinn) < 1: 
           print "Lineage: " + prevlin[0] + " " + tribes[int(prevlin[0])]
           print >> fh3, input4 + "\t" +  prevlin[0] + "\t" + tribes[int(prevlin[0])] 
        elif len(sublinn) > 1:
           for i in range(0,len(prevsub)): 
             split_lin = prevsub[i].split(".")
             if split_lin[0] != prevlin[0]:
               discordance = True
             if split_lin[0] != split_first[0]:
               discordance = True
           if discordance:
              print "no precise lineage inferred"
              print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)"
              sys.exit(1)
           elif animals == False:
              print "Lineage: " + prevlin[0] + " " + tribes[int(prevlin[0])]
              print >> fh3, input4 + "\t" +  prevlin[0] + "\t" + tribes[int(prevlin[0])]
           else:
              print "no precise lineage inferred"
              print >> fh3, input4 + "\t" + "mixed lineage(s)" + "\t" + "mixed lineage(s)"
              sys.exit(1) 
