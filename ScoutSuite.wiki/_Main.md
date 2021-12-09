# What is Scout Suite?
Scout Suite is a security tool that lets AWS, GCP and Azure administrators assess their environment's security posture. Using the cloud environnements' respective APIs, Scout Suite gathers configuration data for manual inspection and highlights high-risk areas automatically. Rather than pouring through dozens of pages on the web, Scout Suite supplies a clear view of the attack surface automatically.

Scout Suite was designed by security consultants/auditor. It is meant to provide a point-in-time security-oriented view of the cloud account it was run in. Once the data has been gathered, all usage may be performed offline.

For engineers in order to implement periodic and/or continuous review of their cloud environment, Scout Suite may be used a base framework that provides. TODO TODO.

## Basic workflow
Assuming access to the cloud APIs has already been configured on a machine (e.g. you can use the AWS CLI for AWS), then installing and using Scout Suite should be trivial:

Install Scout Suite
`pip install scoutsuite`
Run the tool
`Scout (<provider> e.g. aws) (--profile <profile-name>)`
Browse the HTML report that is automatically open in the default web browser
## Advanced usage
1. Generate a list of trusted IP ranges
2. Generate a custom ruleset
3. Provide Scout Suite with the custom ruleset and trusted IP ranges