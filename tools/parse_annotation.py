#! /usr/bin/env python

import sys
import re
from string import join


""" The script accepts a SnpEff annotated VCF file and the sample ID name (string) as input options """
""" it parses files and creates a final annotation file """


input1 = sys.argv[1]
input2 = sys.argv[2]
input3 = sys.argv[3]


position            = ""
reference           = ""
alternate           = ""
annotation          = ""
variant             = ""
read_depth          = ""
perc_alt            = ""
nucleotide_change   = ""
nuc_change          = ""
transcript_pos      = ""
amino_acid_change   = ""
orig_aacid          = ""
new_aacid	    = ""
codon_pos	    = ""
gene_name           = ""
gene_id             = ""
transcript          = ""

(genez,genezid,start,stop,gene_anot,strand) = ([],[],[],[],[],[])
nuc_change  = ""
dic = {'A':'T','T':'A','C':'G','G':'C'}
ref_comp = ""
alt_comp = ""

fh2 = open(input2,'r')
for lines in fh2:
    lined = lines.rstrip("\r\n").split("\t")
    if lines.startswith("H37Rv"):
       continue
    genez.append(lined[0])
    genezid.append(lined[1])
    start.append(lined[2])
    stop.append(lined[3])
    gene_anot.append(lined[4])
    strand.append(lined[5])
fh2.close()
    
fh1 = open(input1,'r')
print "Sample ID" + "\t" + "CHROM" + "\t" + "POS" + "\t" + "REF" + "\t" + "ALT" + "\t" + "Read Depth" + "\t" + "Percent Alt Allele" + "\t" +  "Annotation" + "\t" + "Variant Type" + "\t" + "Nucleotide Change" + "\t" + "Position within CDS " + "\t" + "Amino acid Change" + "\t" + "REF Amino acid" + "\t" + "ALT Amino acid" + "\t" + "Codon Position" + "\t" + "Gene Name" + "\t" + "Gene ID\r" 

for lines in fh1:
    if lines.startswith("#"):
       continue
    fields = lines.rstrip("\r\n").split("\t")
    if fields[6] != "PASS":
       continue
    position = fields[1]
    reference = fields[3]
    alternate = fields[4]
    rarr = fields[9].split(":")
    read_depth = rarr[3]
    perc_alt1 = float(rarr[2])*100.0
    if perc_alt1 < 5.0:
       continue 
    perc_alt = "{0:.2f}".format(perc_alt1)
    subfields = fields[7].split(";")
    if subfields[-1].startswith("ANN"):
       annot = subfields[-1]
    else:
       annot   = subfields[-2]
    subannot   = annot.split(",")
    smallannot = subannot[0].split("|")
    if smallannot[2] == "MODIFIER":
       for x in range(0,3):
           if (int(start[x]) -1) < int(position) < (int(stop[x]) + 1):
              annotation = gene_anot[x]
              if genez[x] == 'rrs':
                 nuc_change = str((int(position)) - (int(start[x]) - 1))
                 gene_id = 'MTB000019'
                 nucleotide_change = "c." + nuc_change + reference + ">" + alternate
              elif genez[x] == 'rrl':
                 nuc_change = str((int(position)) - (int(start[x]) - 1))
                 gene_id = 'MTB000020'
                 nucleotide_change = "c." + nuc_change + reference + ">" + alternate
              elif genez[x] == 'crfA':
                 nuc_change = str((int(position)) - (int(start[x]) - 1))
                 gene_id = 'crfA'
                 nucleotide_change = "c." + nuc_change + reference + ">" + alternate
              elif strand[x] == 'forward':
                 gene_id = genezid[x]
                 nuc_change = str((int(position)) - (int(stop[x]) + 1))
                 nucleotide_change = "c." + nuc_change + reference + ">" + alternate
              elif strand[x] == 'reverse':
                 ref_comp = ""
                 alt_comp = ""
                 for char in reference:
                     ref_comp += dic[char]
                 for char in alternate:
                     alt_comp += dic[char]
                 gene_id = genezid[x]
                 nuc_change = str((int(start[x]) -1) - int(position))
                 nucleotide_change = "c." + nuc_change + ref_comp + ">" + alt_comp
              gene_name = genez[x]
              amino_acid_change  = 'NA'
              if len(fields[4]) > len(fields[3]):
                 if strand[x] == 'forward':
                    nucleotide_change = "c." + nuc_change + "_" + str(int(nuc_change) + 1) + "ins" + alternate[len(reference):]
                    if genez[x] == 'crfA':
                       transcript_pos = nuc_change + "-" + str(int(nuc_change) + 1)
                 elif strand[x] == 'reverse':
                    nucleotide_change = "c." + str(int(nuc_change) - 1) + "_" + nuc_change + "ins" + alt_comp[len(reference):][::-1]  
                 variant = "Insertion"
              elif len(fields[3]) > len(fields[4]):
                 if strand[x] == 'forward':
                    if len(reference) - len(alternate) == 1:
                       nucleotide_change = "c." + str(int(nuc_change) + len(alternate)) + "del" + reference[len(alternate):]
                       if genez[x] == 'crfA':
                          transcript_pos = str(int(nuc_change) + len(alternate))
                    else:
                       nucleotide_change = "c." + str(int(nuc_change) + len(alternate)) + "_" + str(int(nuc_change) + len(reference) - 1) + "del" + reference[len(alternate):]
                       if genez[x] == 'crfA':
                          transcript_pos = str(int(nuc_change) + len(alternate)) + "-" + str(int(nuc_change) + len(reference) - 1)
                 elif strand[x] == 'reverse':
                    if len(reference) - len(alternate) == 1:
                       nucleotide_change = "c." + str(int(nuc_change) - len(reference) - 1) + "del" + ref_comp[len(alternate):][::-1]
                    else:
                       nucleotide_change = "c." + str(int(nuc_change) - len(reference) - 1) + "_" + str(int(nuc_change) - len(alternate))  + "del" + ref_comp[len(alternate):][::-1]
                 variant = "Deletion"
              elif len(fields[3]) > 1 and len(fields[3]) == len(fields[4]):
                   if strand[x] == 'forward':
                      nucleotide_change = "c." + nuc_change + "_" + str(int(nuc_change) + 1) + "del" + reference + "ins" + alternate
                   elif strand[x] == 'reverse':
                      nucleotide_change = "c." + str(int(nuc_change) - 1) + "_" + nuc_change  + "del" + ref_comp[::-1] + "ins" + alt_comp[::-1]
                   variant = "MNP"
              else:
                 variant = "SNP"
              transcript         = 'NA'
              if genez[x] == 'crfA':
                 transcript_pos  = nuc_change
              else:
                 transcript_pos  = 'NA'
              orig_aacid         = 'NA'
              new_aacid	         = 'NA'
              codon_pos	         = 'NA'
              break               
           else:
                (nucposarray,newsubannot) = ([],[])
                indx = len(subannot) - 1
                for x in range(0,indx):
                    nucpos = subannot[x].split("|")[14]
                    if 'downstream' not in subannot[x].split("|")[1] and len(nucpos) > 0 :
                        nucposarray.append(int(nucpos))
                        newsubannot.append(subannot[x])
                if len(newsubannot) > 0:
                   minnuc        = str(min((nucposarray)))
                   ind           = nucposarray.index(int(minnuc))
                   workannot     = newsubannot[ind]
                   newsmallannot = workannot.split("|")
                   nucleotide_change = newsmallannot[9]
                   gene_name         = newsmallannot[3] + ' upstream'
                   gene_id           = newsmallannot[4] + ' upstream'
                else:
                   nucleotide_change = smallannot[9]
                   gene_name         = smallannot[3] + ' downstream'
                   gene_id           = smallannot[4] + ' downstream'
                annotation           = 'Non-Coding'
                if len(fields[3]) > len(fields[4]):
                   variant         = 'Deletion'
                elif len(fields[4]) > len(fields[3]):
                   variant         = 'Insertion'
                elif len(fields[3]) > 1 and len(fields[3]) == len(fields[4]):
                   variant         = 'MNP'
                else:
                   variant         = 'SNP'
                amino_acid_change  = 'NA'
                transcript         = 'NA'
                transcript_pos     = 'NA'
                orig_aacid         = 'NA'
                new_aacid	   = 'NA'
                codon_pos	   = 'NA'
       print  input3 + "\t" + fields[0] + "\t" + position + "\t" + reference + "\t" + alternate + "\t" + read_depth + "\t" + perc_alt + "\t" + annotation + "\t" + variant + "\t" + nucleotide_change + "\t" + transcript_pos + "\t" + amino_acid_change + "\t" + orig_aacid + "\t" + new_aacid + "\t" + codon_pos + "\t" + gene_name + "\t" + gene_id + "\r"
    
    else:
        if len(smallannot[10]) < 13:
           if smallannot[10][2:5] == smallannot[10][-3:]:
              annotation = 'Synonymous'
           else:
              annotation = 'Non-synonymous'
        elif len(smallannot[10]) > 13:
             pos11    = re.findall(r'\d+', smallannot[10])
             ind11    = smallannot[10].index(pos11[0])
             ind11len = len(pos11[0])
             translen = ind11 + ind11len
             if smallannot[10][2:ind11] == smallannot[10][translen:]:
                annotation = 'Synonymous'
             else:
                annotation = 'Non-synonymous'  
        nucleotide_change  = smallannot[9]
        if len(smallannot[10]) < 1:
           amino_acid_change  = "NA"
        else:
           amino_acid_change  = smallannot[10]
        gene_name          = smallannot[3]
        gene_id            = smallannot[4]
        transcript         = smallannot[6]
        if gene_name == 'erm_37_':
           gene_name = 'erm(37)'
        if len(fields[3]) == len(fields[4]) and len(fields[3]) > 1:
           variant = 'MNP'
        elif 'del' in nucleotide_change or 'del' in amino_acid_change:
           variant = 'Deletion'
        elif 'ins' in nucleotide_change or 'ins' in amino_acid_change:
            variant = 'Insertion'
        elif 'dup' in nucleotide_change or 'dup' in amino_acid_change:
           variant = 'Insertion'
        else:
            variant = 'SNP'
        if variant == 'Insertion' or variant == 'Deletion':
           new_aacid = 'NA'
           if '_' in smallannot[9]:
              array1 = smallannot[9].split("_")
              po1 = array1[0].split(".")
              pos1 = po1[1]
              pos2 = re.findall(r'\d+', array1[1])[0]
              transcript_pos = pos1 + "-" + pos2
           else:
              transcript_pos = re.findall(r'\d+', smallannot[9])[0]
           if '_' in smallannot[10]:
              array2 = smallannot[10].split("_")
              po11 = array2[0].split(".")
              orig_aacid = po11[1][0:3]
              pos11  = po11[1][3:]
              pos12  = re.findall(r'\d+', array2[1])[0]
              codon_pos = pos11 + "-" + pos12
           
           else:
              if len(smallannot[10]) > 0:
                 codon_pos = re.findall(r'\d+', smallannot[10])[0]
                 orig_aacid = smallannot[10][2:5]
              else:
                  codon_pos =  "NA"
                  orig_aacid = "NA"     
        else :
            if len(smallannot[10]) < 13:
               orig_aacid = smallannot[10][2:5]
            elif len(smallannot[10]) > 13:
               pos11      = re.findall(r'\d+', smallannot[10])
               ind11      = smallannot[10].index(pos11[0])
               orig_aacid = smallannot[10][2:ind11]  
            if '*' in smallannot[10] or '?' in smallannot[10] :
               new_aacid  = 'NA'
            else:
               if len(smallannot[10]) < 13:
                  new_aacid  = smallannot[10][-3:]
               elif len(smallannot[10]) > 13:
                  pos11      = re.findall(r'\d+', smallannot[10])
                  ind11      = smallannot[10].index(pos11[0])
                  transpos   = len(pos11[0]) + ind11
                  new_aacid  = smallannot[10][transpos:] 
            transcript_pos   = re.findall(r'\d+', smallannot[9])[0]
            if len(smallannot[10]) < 13:
               codon_pos     = re.findall(r'\d+', smallannot[10])[0]
            elif len(smallannot[10]) > 13:
               string_pos       = re.findall(r'\d+', smallannot[10])[0]
               string_pos_2     = int(string_pos) + 1
               codon_pos        = string_pos + "-" + str(string_pos_2)
            
        for x in range(0,3):
           if (int(start[x]) -1) < int(position) < (int(stop[x]) + 1):
              annotation = gene_anot[x]    
              if strand[x] == 'forward':
                 gene_id  =  genezid[x]
                 nuc_change = str((int(position)) - (int(stop[x]) + 1))
                 nucleotide_change = "c." + nuc_change + reference + ">" + alternate
              elif strand[x] == 'reverse':
                 ref_comp = ""
                 alt_comp = ""
                 for char in reference:
                     ref_comp += dic[char]
                 for char in alternate:
                     alt_comp += dic[char]
                 gene_id  =  genezid[x]
                 nuc_change = str((int(start[x]) -1) - int(position))
                 nucleotide_change = "c." + nuc_change + ref_comp + ">" + alt_comp
              gene_name = genez[x]
              amino_acid_change  = 'NA'
              if len(fields[4]) > len(fields[3]):
                 if strand[x] == 'forward':
                    nucleotide_change = "c." + nuc_change + "_" + str(int(nuc_change) + 1) + "ins" + alternate[len(reference):]
                 elif strand[x] == 'reverse':
                    nucleotide_change = "c." + str(int(nuc_change) - 1) + "_" + nuc_change + "ins" + alt_comp[len(reference):][::-1]
                 variant = "Insertion"
              elif len(fields[3]) > len(fields[4]):
                 if strand[x] == 'forward':
                    if len(reference) - len(alternate) == 1:
                       nucleotide_change = "c." + str(int(nuc_change) + len(alternate)) + "del" + reference[len(alternate):]
                    else:
                       nucleotide_change = "c." + str(int(nuc_change) + len(alternate)) + "_" + str(int(nuc_change) + len(reference) - 1) + "del" + reference[len(alternate):]
                 elif strand[x] == 'reverse':
                    if len(reference) - len(alternate) == 1:
                       nucleotide_change = "c." + str(int(nuc_change) - len(reference) - 1) + "del" + ref_comp[len(alternate):][::-1]
                    else:
                       nucleotide_change = "c." + str(int(nuc_change) - len(reference) - 1) + "_" + str(int(nuc_change) - len(alternate))  + "del" + ref_comp[len(alternate):][::-1]
                 variant = "Deletion"
              elif len(fields[3]) > 1 and len(fields[3]) == len(fields[4]):
                   if strand[x] == 'forward':
                      nucleotide_change = "c." + nuc_change + "_" + str(int(nuc_change) + 1) + "del" + reference + "ins" + alternate
                   elif strand[x] == 'reverse':
                      nucleotide_change = "c." + str(int(nuc_change) - 1) + "_" + nuc_change  + "del" + ref_comp[::-1] + "ins" + alt_comp[::-1]
                   variant = "MNP"
              else:
                 variant = "SNP"
              transcript         = 'NA'
              transcript_pos     = 'NA'
              orig_aacid         = 'NA'
              new_aacid          = 'NA'
              codon_pos          = 'NA'
              break
        print input3 + "\t" + fields[0] + "\t" + position + "\t" + reference + "\t" + alternate + "\t" + read_depth + "\t" + perc_alt + "\t" + annotation + "\t" + variant + "\t" + nucleotide_change + "\t" + transcript_pos + "\t" + amino_acid_change + "\t" + orig_aacid + "\t" + new_aacid + "\t" + codon_pos + "\t" + gene_name + "\t" + gene_id + "\r"

fh1.close()

