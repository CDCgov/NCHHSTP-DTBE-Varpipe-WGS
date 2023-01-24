#!/bin/bash
#
# Title: get_gatk.sh
# Description:
# Usage:
# Date Created: 2023-01-23 14:30
# Last Modified: Mon 23 Jan 2023 02:35:00 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

DL_URL='https://github.com/broadinstitute/gatk/releases/download/4.2.4.0/gatk-4.2.4.0.zip'

mkdir tmp
cd tmp
wget -O- $URL >gatk-4.2.4.0.zip
unzip gatk-4.2.4.0.zip
mv gatk-package-4.2.4.0-local.jar ../tools/gatk-4.2.4.0/
