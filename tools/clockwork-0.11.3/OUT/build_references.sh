#!/usr/bin/env bash
#
# Title: build_references.sh
# Description: Combines the downloaded reference files and creates a BWA index
# Usage: Used by setup.sh
# Date Created: 2023-01-23 20:21
# Last Modified: Mon 18 Dec 2023 05:24:54 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

gunzip ref.??.fa.gz

cat ref.??.fa >ref.fa

rm ref.??.fa

../../bwa index -b 100000000 ref.fa
