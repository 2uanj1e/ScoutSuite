# Basic Usage

The following command will provide the list of available command line options:

    $ python scout.py --help

You can also use this to get help on a specific provider:

    $ python scout.py PROVIDER --help

After performing a number of API calls, Scout will create a local HTML report and open it in the default browser.

Also note that the command line will try to infer the argument name if possible when receiving partial switch. For
example, this will work and use the selected profile:

    $ python scout.py aws --profile PROFILE

## Credentials

Assuming you already have your provider's CLI up and running you should have your credentials already set up and be able to run Scout Suite by using one of the following commands. If that is not the case, please consult the wiki page for the provider desired.

### [Amazon Web Services](https://github.com/nccgroup/ScoutSuite/wiki/Amazon-Web-Services)

    $ python scout.py aws

### [Azure](https://github.com/nccgroup/ScoutSuite/wiki/Azure)

    $ python scout.py azure --cli

### [Google Cloud Platform](https://github.com/nccgroup/ScoutSuite/wiki/Google-Cloud-Platform)

    $ python scout.py gcp --user-account