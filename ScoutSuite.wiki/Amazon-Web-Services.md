# Amazon Web Services <img src="https://user-images.githubusercontent.com/4206926/63152064-39e51b00-c00b-11e9-921f-602de55f44d3.png" width="10%"></img>

# Introduction

Scout Suite was designed to work seamlessly on machines used to make AWS API calls, which includes

1. Developer machines configured to use the AWS CLI or any other tool based on AWS official SDKs.
2. EC2 instances

In the following section, we will discuss in further details various configurations for AWS.

**It is important to note that Scout leverages [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) to handle authentication. When in doubt, please refer to this document.**

## Simple usage

Using a computer already configured to use the AWS CLI (i.e. `default` profile), you may use Scout using the following command:

```bash
$ python scout.py aws
```

**Note:** EC2 instances with an IAM role fit in this category.

## Authentication

### AWS Credentials File

If you've used the AWS CLI or any tool based on one of the AWS SDKs, chances are you have configured your environment such that credentials are ready to be used. This could be the result from running the `aws configure` command, for example. In practice, your AWS credentials are stored in a file under `~/.aws/credentials`.

```
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = foobar
```

This means that, if you run a command such as `aws iam list-users`, the credentials will be read from the `default` profile. For users who interact with multiple AWS accounts, AWS allows to have profiles. This would result in a configuration file looking as follow.

```
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = foobar
[profile1]
aws_access_key_id = AKIA...
aws_secret_access_key = foobar1
[profile2]
aws_access_key_id = AKIA...
aws_secret_access_key = foobar2
```

In this configuration, users may now run the AWS CLI and choose the pair of credentials with the `--profile <profilename>` argument, where profile name would be `profile1` or `profile2`. Similar to the AWS CLI, Scout Suite supports profiles and could be run using the credentials associated with any of these profiles.

### AWS Credentials File with MFA

If MFA-protected API access has been enabled in your account, use of the access key ID and secret key may be limited to several actions until STS credentials have been obtained. Please consult [this page](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/) in order to 
configure MFA authentication through the management of session tokens.

### AWS Credentials File with Roles

A common way to access the AWS APIs now is to assume a particular role, receive a new set of STS credentials, and use these for subsequent API calls. Scout Suite supports this functionality as well. The easiest way to use IAM roles with Scout Suite (and the AWS CLI) is to configure a new profile in the `~/.aws/config` file, as illustrated below.

```
[profile profile1-demorole]
role_arn = arn:aws:iam::123456789012:role/Demo
source_profile = profile1
[profile profile2-demorole]
role_arn = arn:aws:iam::0987654321098:role/Demo
source_profile = profile2
```

In this example, two IAM roles have been configured and associated with a profile for which credentials have already been configured in the `~/.aws/credentials` file. Using Scout Suite (or the AWS CLI) with the `--profile profile1-demorole` will result in an API call to `sts:assumerole` be made, short-lived credentials be stored under the `~/.aws/cli/cache` folder, and the tool to run in the role's context.

### Environment Variables

If credentials have been configured as environment variables, Scout Suite will use these when making API calls.

```bash
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### CLI Parameters

You can launch an Scout Suite as so:
```sh
$ python scout.py aws --access-keys --access-key-id <AKIAIOSFODNN7EXAMPLE> --secret-access-key <wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY> --session-token <token>
```

The `--session-token` is optional and only used for temporary credentials (i.e. role assumption).

## Permissions

The following AWS Managed Policies can be attached to the principal used to run Scout in order to grant the necessary
permissions:

-   `ReadOnlyAccess`
-   `SecurityAudit`

You will also find a custom policy to run Scout with minimal privileges [here](https://github.com/nccgroup/ScoutSuite/wiki/AWS-Minimal-Privileges-Policy).