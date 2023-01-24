#!/usr/bin/env bash
#
# Title: build_signularity.sh
# Description:
# Usage:
# Date Created: 2023-01-11 13:28
# Last Modified: Wed 11 Jan 2023 01:34:16 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#

if [[ ${1} == 'with_references' ]]; then
    echo 'Building singularity image with references included'
    singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
else
    echo 'Building singularity image without references included'
    singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_without_refs:latest
fi

