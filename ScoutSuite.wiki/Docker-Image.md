## Quick Links

1. [Running the Container](#running-thecontainer)
1. [Running Scoutsuite](#running-scoutsuite)
    1. [Example Test](#example-test)
1. [Accessing the Report](#report-access)

## Overview

This image is an Ubuntu based container that comes with all pre-requisite software required to run ScoutSuite. It's based on the Ubuntu 20.04 docker base. 

The following CLI tools are also installed:

* **AWS (version 2)**:

~~~bash
aws-cli/2.1.29 Python/3.8.8 Linux/4.19.121-linuxkit exe/x86_64.debian.10 prompt/off
~~~

* **Azure**:  

~~~bash
azure-cli                         2.20.0

core                              2.20.0
telemetry                          1.0.6

Python location '/opt/az/bin/python3'
Extensions directory '/root/.azure/cliextensions'

Python (Linux) 3.6.10 (default, Feb 26 2021, 06:44:08)
[GCC 8.3.0]
~~~

* **GCP**:

~~~bash
Google Cloud SDK 330.0.0
alpha 2021.02.26
app-engine-python 1.9.91
app-engine-python-extras 1.9.91
beta 2021.02.26
bq 2.0.65
core 2021.02.26
gsutil 4.59
~~~

----

<a name="running-thecontainer" href="#"></a>

## Running The Container

There are two ways to run the ScoutSuite Docker image: 

1. Grab the image from DockerHub and run it: `docker run -it rossja/ncc-scoutsuite`
1. Build the container from this source:
   1. Clone the [ScoutSuite GitHub Repo](https://github.com/nccgroup/ScoutSuite)
   1. Change to the `ScoutSuite/docker` directory
   1. Run `docker-compose up --build` to create the container
   1. Run ScoutSuite in the container using `docker run -it scoutsuite`.

----

<a name="running-scoutsuite" href="#"></a>

## Running ScoutSuite

Once the CLI for the environment you are testing has been configured and the appropriate credentials set up (see the wiki for more info on how to do this), you can run ScoutSuite in the container. As of version 0.1.0, when you run the container you're automatically set up in the scoutsuite environment.

You should see that the command prompt reflects this virtual environment, with the name of the virtual environment (scoutsuite) preceding the root prompt: `(scoutsuite) root@1350ede02c47:~#`

If you need to manually restart the virtual environment, you can do this using the activate script in `/root/scoutsuite/bin/activate`: 

~~~bash
root@1350ede02c47:~# source scoutsuite/bin/activate
(scoutsuite) root@1350ede02c47:~#
~~~

### Recommended Runtime Parameters

* Since this is a container, there's no GUI, and no browser, so passing the `--no-browser` probably makes sense. 
* Likewise, setting a specific report directory using something like `--report-dir /root/scout-report` is a good idea. *(The default location is `$HOME/scoutsuite-report`)*

----

<a name="example-test" href="#"></a>

## Example Test

The example below demonstrates running scout against AWS, using the profile `scout-user01`, saving the report to the directory `/root/scout-report`: 

~~~bash
scout aws --profile scout-user01 --no-browser --report-dir /root/scout-report
2020-01-03 17:45:16 460837197ae9 scout[7087] INFO Launching Scout
2020-01-03 17:45:16 460837197ae9 scout[7087] INFO Authenticating to cloud provider
2020-01-03 17:45:17 460837197ae9 scout[7087] INFO Gathering data from APIs
2020-01-03 17:45:17 460837197ae9 scout[7087] INFO Fetching resources for the Lambda service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudFormation service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudTrail service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the CloudWatch service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the Config service
2020-01-03 17:45:18 460837197ae9 scout[7087] INFO Fetching resources for the Direct Connect service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the EC2 service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the EFS service
2020-01-03 17:45:19 460837197ae9 scout[7087] INFO Fetching resources for the ElastiCache service
2020-01-03 17:45:20 460837197ae9 scout[7087] INFO Fetching resources for the ELB service
2020-01-03 17:45:21 460837197ae9 scout[7087] INFO Fetching resources for the ELBv2 service
2020-01-03 17:45:21 460837197ae9 scout[7087] INFO Fetching resources for the EMR service
2020-01-03 17:45:22 460837197ae9 scout[7087] INFO Fetching resources for the IAM service
2020-01-03 17:45:22 460837197ae9 scout[7087] INFO Fetching resources for the RDS service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the RedShift service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the Route53 service
2020-01-03 17:45:23 460837197ae9 scout[7087] INFO Fetching resources for the S3 service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SES service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SNS service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the SQS service
2020-01-03 17:45:24 460837197ae9 scout[7087] INFO Fetching resources for the VPC service
2020-01-03 17:46:13 460837197ae9 scout[7087] INFO Running rule engine
2020-01-03 17:46:15 460837197ae9 scout[7087] INFO Applying display filters
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Saving data to /root/scout-report/scoutsuite-results/scoutsuite_results_aws-scout-user01.js
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Saving data to /root/scout-report/scoutsuite-results/scoutsuite_exceptions_aws-scout-user01.js
2020-01-03 17:46:16 460837197ae9 scout[7087] INFO Creating /root/scout-report/aws-scout-user01.html
~~~

----

<a name="report-access" href="#"></a>

## Accessing Report Data

The report is stored in the directory specified with the `--report-dir` flag.

*Note: if this flag is omitted, the default is to create a `scoutsuite-report` directory in the directory the user is in at the time scout is run*.

### TL;DR

You can shortcut the process below by simply combining the `docker ps` command with the `docker cp` command like so: 

~~~bash
docker cp $(docker ps -f ancestor=rossja/ncc-scoutsuite --format "{{.ID}}"):/root/scout-report ./
~~~

### Details

To copy the report data out of the running container, you can use the following process:

* On the docker host (not the container): run `docker ps` using a filter to find the container ID for the running instance of the container. An example of how to do this is shown below:

~~~bash
docker ps -f ancestor=rossja/ncc-scoutsuite --format "Container ID: {{.ID}}"
Container ID: a8d70ee4ced8
~~~

* Once you have the container ID, you can use the `docker cp` command to copy the report from the running container instance to your Docker host:

~~~bash
docker cp <container-id>:</path/to/report> </path/to/local/copy>
~~~

* For example, if the container ID is `a8d70ee4ced8`, and the report is stored in `/root/scout-report` on that container, the following command could be used to copy the report data from the container to the current directory: 

~~~bash
docker cp a8d70ee4ced8:/root/scout-report ./
~~~

You can shortcut this process by simply combining the `docker ps` command with the `docker cp` command like so: 

~~~bash
docker cp $(docker ps -f ancestor=rossja/ncc-scoutsuite --format "{{.ID}}"):/root/scout-report ./
~~~

----


## Viewing the Output File

The report itself can be viewed using a web browser, by opening the file `./scout-report/aws-<profile>.html`. 

For example, if you ran the scout tool against AWS using the profile `scout-user01`, the report HTML file is at `./scout-report/aws-scout-01.html`. 

**NOTES**: 

**AWS**: If you used the default AWS profile credentials, the profile name is the numerical ID portion of the ARN for the user, rather than a specific profile or user name.

**GCP**: The scout report will be named using the project ID that was passed in.