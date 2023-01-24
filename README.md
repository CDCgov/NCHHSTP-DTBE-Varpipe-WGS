# Installing and Using the varpipe_wgs pipeline #

## Overview ##

# Installing and Using the varpipe_wgs pipeline #

This repository contains the Varpipe_wgs pipeline developed by the Division of TB Elimination. The pipeline cleans the data and performs analyses, including typing and variant detection. While originally build to analyze Tuberculosis data, the pipeline accepts other references, allowing it be used more broadly.

End users can run the pipeline using [docker](#use-docker), [singularity](#use-singularity), or their [local](#use-local) machine.

## Prepare the Data ##                 

First, copy the gzipped fastq files you wish to analyze to the data/ directory in this repository

## Use Docker ##

### Start the container ###

To use Docker to run the pipeline, first choose whether you will use the container image with or without references included.

To use the image with references, run the following commands

```console
docker pull ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
docker run -it -v <path to data>:/varpipe_wgs/data ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
```

To use the image without references you will need to change the container name in the command to varpipe_wgs_without_refs:latest, and you will also need to specify a folder with the references to be used by clockwork. This folder must be mounted to the container as /varpipe_wgs/tools/clockwork-0.11.3/OUT.

```console
docker pull ghcr.io/cdcgov/varpipe_wgs_with_refs:latest
docker run -it -v <path to data>:/varpipe_wgs/data -v <path to references>:/varpipe_wgs/tools/clockwork-0.11.3/OUT ghcr.io/cdcgov/varpipe_wgs_without_refs:latest
```

### Run the pipeline ###

Those commands will download the most recent version of the pipeline and then start the container and connect to it.

When connected to the container you will be in the directory /varpipe_wgs/data. From there simply start the pipeline with the command

```console
cd /varpipe_wgs/data
./runVarpipeline.sh
```

That will identify all gzipped fastq files in the directory and run the pipeline over them, creating a results folder named "Output_\<MM\>_\<DD\>_\<YYYY\>"

When the pipeline is finished you can disconnect from and close the container by pressing CTRL+D. You can then review the results.


## Use Singularity ##

### Obtain the Singularity image ###

The singularity images are too large to include in this repository, but the version with references is available on Singularity Container Library. To access you, run the command 


```console
singularity pull library://reagank/varpipe_wgs/pipeline_with_references
```

The Singularity images can also be built locally using the provided build_singularity.sh script.

```console
./build_singularity.sh
```

The script builds the image without references by default, to build the image including references provide the argument "with_references"

```console
./build_singularity.sh with_references
```

## Start the Singularity image ###

Once you have downloaded or built the .sif file containing the singularity image, the command to start and connect to the container that includes references is:

```console
singularity shell --bind <path to data>:/varpipe_wgs/data pipeline_with_refs.sif
```

As with Docker, to run the pipeline without references you will need to supply clockwork compatible references and bind it to the image as the /varpipe_wgs/tools/clockwork-0.11.3/OUT directory

```console
singularity shell --bind ./data:/varpipe_wgs/data --bind <path-to-references>:/varpipe_wgs/tools/clockwork-0.11.3/OUT pipeline_without_refs.sif
```

Please note, if you are running this pipeline using CDC SciComp resources then security settings will require specifying the SINGULARITY_TMPDIR environmental variable like this: 

```console
SINGULARITY_TMPDIR=~/.tmp singularity shell --bind ./data:/varpipe_wgs/data --bind <path-to-references>:/varpipe_wgs/tools/clockwork-0.11.3/OUT pipeline_without_refs.sif
```

### Run the pipeline ###

This command starts the container and connect to it.

When connected to the container you will be in your home directory. You must cd to the directory /varpipe_wgs/data. From there start the pipeline with the command

```console
cd /varpipe_wgs/data
./runVarpipeline.sh
```

That will identify all gzipped fastq files in the directory and run the pipeline over them, creating a results folder named "Output_\<MM\>_\<DD\>_\<YYYY\>"

When the pipeline is finished you can disconnect from and close the container by pressing CTRL+D. You can then review the results.

## Use Local ##

### Prerequisites

To run the pipeline locally, you will need to have the following programs installed:

 - Python 2.7
 - Java 1.8
 - Singularity >=3.5

The remaining programs used by the pipeline are included in this repository in the tools/ directroy.

### Install the Pipeline

First, clone and dowload this repository with the command

```console
git clone https://github.com/CDCGov/NCHHSTP-DTBE-Varpipe-WGS.git
```
Then, simply run setup.sh to finish the installation. This script runs several steps:

 - Downloads the clockwork singularity image
 - Downloads GATK
 - Builds a reference fasta and creates BWA indexes


Latly, update the script tools/clockwork-0.11.3/clockwork script to correctly point to the clockwork 0.11.3 image

### Run the Pipeline ###

After the data has been added to the data/ directory, cd into data/ and run the pipeline with the commands

```console
cd data/
./runVarpipeline.sh
```

That will identify all gzipped fastq files in the directory and run the pipeline over them, creating a results folder named "Output_\<MM\>_\<DD\>_\<YYYY\>"

## Public Domain Standard Notice
This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

## License Standard Notice
The repository utilizes code licensed under the terms of the Apache Software
License and therefore is licensed under ASL v2 or later.

This source code in this repository is free: you can redistribute it and/or modify it under
the terms of the Apache Software License version 2, or (at your option) any
later version.

This source code in this repository is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the Apache Software License for more details.

You should have received a copy of the Apache Software License along with this
program. If not, see http://www.apache.org/licenses/LICENSE-2.0.html

The source code forked from other open source projects will inherit its license.

## Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md)
and [Code of Conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

## Contributing Standard Notice
Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).

## Records Management Standard Notice
This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

## Additional Standard Notices
Please refer to [CDC's Template Repository](https://github.com/CDCgov/template)
for more information about [contributing to this repository](https://github.com/CDCgov/template/blob/master/CONTRIBUTING.md),
[public domain notices and disclaimers](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md),
and [code of conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
