#!/usr/bin/env bash
#
# Title: build_new_index.sh
# Description: Builds a BWA index for a reference file
# Usage: ./build_new_index.sh
# Date Created: 2023-12-19 13:57
# Last Modified: Tue 19 Dec 2023 01:58:16 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

../../bwa index -b 100000000 ref.fa
