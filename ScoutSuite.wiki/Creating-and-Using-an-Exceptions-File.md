# Introduction

In addition to supporting custom rules and custom rulesets, Scout Suite enables users to flag certain resources as exceptions. For example, you may want to mark the S3 bucket that receives S3 access logs as an exception to the rule flagging S3 buckets for which access logs has not been enabled. This wiki page illustrates how one may generate a list of exceptions and use it when running the Scout Suite analysis.

# Step 1: Creation of a list of exceptions

The Scout Suite HTML report is the UI that may be used to create a list of exceptions. The following screenshot is from the IAM dashboard in an AWS account:

![sc_2020-05-28_12h27m15s](https://user-images.githubusercontent.com/4206926/83130637-eeee4d00-a0de-11ea-801b-a31d65c1f173.png)

In this example, we will mark the first finding as an exception.

The first step is to click on this dashboard element to display the list of resources flagged by the rule. In this case, two roles are not compliant:

![sc_2020-05-28_12h31m25s](https://user-images.githubusercontent.com/4206926/83130987-73d96680-a0df-11ea-99bf-23801ceff347.png)

We will exclude the second one (`test-role`).  After clicking on the trust policy details, we see that the flagged statement is hilighted:

![sc_2020-05-28_12h34m27s](https://user-images.githubusercontent.com/4206926/83131154-b438e480-a0df-11ea-86de-e77acb2eb474.png)

Clicking on the element highlighted in red will cause a JavaScript box to be displayed, asking whether this resource should be added to the list of exceptions for this particular rule:

![sc_2020-05-28_12h35m52s](https://user-images.githubusercontent.com/4206926/83131986-01698600-a0e1-11ea-833d-158ab89abf33.png)

Clicking on the "OK" button will update the list of exceptions; however, the Scout Suite results have not been updated at this time. In order to take the list of exceptions in account, you must click on the "Help" drop down menu and select the "Export Exceptions" option.

![sc_2020-05-28_12h36m41s](https://user-images.githubusercontent.com/4206926/83131994-04fd0d00-a0e1-11ea-9e35-d7ee9d0b5213.png)

This will make the browser download the exceptions file.

# Step 2: Run Scout Suite with a list of exceptions

Once the exceptions file has been generated and downloaded, you can provide it to Scout. In order to update the report, you will need to re-run Scout. Because all the configuration has been fetched already, there is no need to re-run a full scan - a local run may be performed with the following command:

```
$ python scout.py aws --profile <profile-name> --local --exceptions /path/to/exceptions.json --no-browser
```

The `--no-browser` option means that Scout Suite will not open the report in a new browser window, this is optional. If you choose to do so, you then need to refresh the Scout Suite report in your browser. When navigating to the resources affected by the IAM issue, you will be able to confirm that the list of exceptions has been taken in account:

![sc_2020-05-28_12h42m13s](https://user-images.githubusercontent.com/4206926/83131998-06c6d080-a0e1-11ea-8d65-08c9cd1686a3.png)

Note that, from here, if you choose to generate a new list of exception. The list of exceptions that you will generate will include the exceptions used during the last run, as well as the exceptions just set in the UI.