#!/usr/bin/env bash
#
# Title: build_signularity.sh
# Description: This script builds a Singularity image from a docker image.
# Usage: ./build_signularity.sh [with_references|without_references]
# Date Created: 2023-01-11 13:28
# Last Modified: Tue 19 Dec 2023 06:20:20 PM EST
# Author: Reagan Kelly (ylb9@cdc.gov)
#


# NOTE: The "SINGULARITY_TMPDIR=~/.tmp" is only required if your system has "noexec" set on the /tmp mount
if [[ ${1} == 'with_references' ]]; then
    echo 'Building singularity image with references included'
    SINGULARITY_TMPDIR=~/.tmp singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
elif [[ ${1} == 'without_references' ]]; then
    echo 'Building singularity image without references included'
    SINGULARITY_TMPDIR=~/.tmp singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_without_refs:latest
else
    echo 'Building singularity images with and without references included'
    echo 'Building singularity image with references included'
    SINGULARITY_TMPDIR=~/.tmp singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
    echo 'Building singularity image without references included'
    SINGULARITY_TMPDIR=~/.tmp singularity build pipeline_with_references.sif docker://ghcr.io/cdcgov/varpipe_wgs_without_refs:latest
fi

