#!/usr/bin/env bash
#
# Title: setup.sh
# Description:
# Usage:
# Date Created: 2023-01-24 11:49
# Last Modified: Tue 24 Jan 2023 11:50:07 AM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

./get_clockwork.sh
./get_gatk.sh
pushd tools/clockwork-0.11.3/OUT
./build_references.sh
popd
