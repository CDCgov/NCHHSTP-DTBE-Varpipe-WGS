#!/usr/bin/env bash
#
# Title: build_references.sh
# Description:
# Usage:
# Date Created: 2023-01-23 20:21
# Last Modified: Mon 23 Jan 2023 08:26:17 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

gunzip ref.??.fa.gz

cat ref.??.fa >ref.fa

../../bwa index -b 100000000 ref.fa
