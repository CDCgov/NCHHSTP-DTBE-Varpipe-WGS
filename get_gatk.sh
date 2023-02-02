#!/bin/bash
#
# Title: get_gatk.sh
# Description:
# Usage:
# Date Created: 2023-01-23 14:30
# Last Modified: Wed 25 Jan 2023 10:02:39 AM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

DL_URL='https://github.com/broadinstitute/gatk/releases/download/4.2.4.0/gatk-4.2.4.0.zip'

mkdir tmp
cd tmp
wget -O- $DL_URL >gatk-4.2.4.0.zip
unzip gatk-4.2.4.0.zip
mv gatk-4.2.4.0/gatk-package-4.2.4.0-local.jar ../tools/gatk-4.2.4.0/
cd ../
rm -rf tmp/
