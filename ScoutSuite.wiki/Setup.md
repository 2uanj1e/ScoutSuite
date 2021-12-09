# Requirements

Assuming access to the desired APIs has already been configured on a machine (_e.g._ the provider's CLI has been set up), then installing and using Scout Suite should be trivial.

Scout Suite is written in Python and supports the following versions:

-   3.6
-   3.7
-   3.8

The required libraries can be found in the
[requirements.txt](https://github.com/nccgroup/ScoutSuite/blob/master/requirements.txt) file.

We recommend using a virtual environment.

# Installation

## Via PIP

```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install scoutsuite
$ scout --help
```

### Demo

![Installation via pip](https://user-images.githubusercontent.com/13310971/78389081-209bd980-75b0-11ea-9a17-dc75c639db2a.gif)

## Via Git

```sh
$ git clone https://github.com/nccgroup/ScoutSuite
$ cd ScoutSuite
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python scout.py --help
```

# Computing resources

Scout Suite is a multi-threaded tool that fetches and stores your cloud account's configuration settings in memory during runtime. It is expected that the tool will run with no issues on any modern laptop or equivalent VM. 

**Note** that running Scout Suite in a VM with limited computing resources such as an AWS `t2.micro` instance is not intended and may result in the process being killed.

# OSX

Due to the fact that by default, OSX only allows for a small number of open file descriptors, users may get the following error:

```console
[Errno 8] nodename nor servname provided, or not known
```

A quick fix is to increase this limit with:

```console
$ ulimit -Sn 1000
```
