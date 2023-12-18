#!/bin/bash
#
# Title: get_gatk.sh
# Description: Retrieves GATK for the pipeline to use
# Usage: Used by setup.sh
# Date Created: 2023-01-23 14:30
# Last Modified: Mon 18 Dec 2023 05:22:54 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

DL_URL='https://github.com/broadinstitute/gatk/releases/download/4.2.4.0/gatk-4.2.4.0.zip'

mkdir tmp
pushd tmp
wget -O- $DL_URL >gatk-4.2.4.0.zip
unzip gatk-4.2.4.0.zip
mv gatk-4.2.4.0/gatk-package-4.2.4.0-local.jar ../tools/gatk-4.2.4.0/
popd
rm -rf tmp/
