#!/bin/bash -l
#
# Title: split_references.sh
# Description: Used to split the ref.fa file into 50 smaller fasta files for inclusion in the git repository
# Usage: ./split_references.sh
# Date Created: 2023-12-18 17:37
# Last Modified: Tue 19 Dec 2023 01:44:03 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

# This script requires the software pyfasta. Install it using pip install pyfasta.

pyfasta split -n50 ref.fa

gzip ref.??.fa

rm ref.fa.flat ref.fa.gdx
