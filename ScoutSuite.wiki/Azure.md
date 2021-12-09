# Azure <img src="https://user-images.githubusercontent.com/17322874/55969424-c477d100-5c4b-11e9-9e51-90ff16c2e6cb.png" width="5%"></img>

# Table of contents
* [Authentication](#Authentication)
* [Permissions](#Permissions)
* [Options](#Options)

## Authentication

There are a number of ways to run Scout against an Azure tenant.

### Supported Methods

#### azure-cli

1. On most system, you can install azure-cli using `pip install azure-cli`
2. Log into an account
   1. The easiest way to do it it with `az login`(for more authentication method,
you can refer to https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest)
3. Run Scout with the `--cli` flag

#### User Credentials

1. Run Scout using `--user-account`
2. Scout will prompt you for your credentials

##### User Credentials via Browser

1. Run Scout using `--user-account-browser`
2. Through a browser, pick your azure account

This authentication method is mostly useful for users which have MFA enabled.

#### Service Principal

1. Set up a Service Principal on the Azure portal (you can refer to
    https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
2. Run Scout with the `--service-principal` flag.
3. Scout will prompt you for the required information

##### File-Based Authentication

1. Create a Service Principal for azure SDK. You can do this with `azure-cli` by running:
```sh
az ad sp create-for-rbac --sdk-auth > mycredentials.json
```
2. Run Scout while providing it with the credentials file using
    `--file-auth path/to/mycredentials.json`

#### Managed Service Identity

1. Configure your identity on the Azure portal (you can refer to
    https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/)
2. Run Scout with the `--msi` flag

### MFA

To run Scout Suite against an Azure user with MFA enabled, there are two options:

- Azure CLI
  - Install the CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
  - Run `az login` to log the CLI into your account. This will open a web browser and let you log in
  - Run Scout with the Azure `--cli` option
- User Browser Login
  - Run Scout with the Azure `--user-account-browser` option
  - Through a browser, pick your azure account

## Permissions

Scout will require that the provided credentials have the `Reader` and `Security Reader` roles in all the subscriptions to assess:

1. Create a user in the desired directory
2. Grant the given user the role of Global Reader in the directory
3. Add the user to the desired subscription, with both `Reader` and `Security Reader` roles

### v5

When using a Scout Suite **v5** or below. Additionally, when running Scout with Service Principals, the following [Azure Active Directory Graph API
application permissions](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-graph-api) are required:

- `Directory.Read.All`

The following screenshot shows the required configuration:
![Service Principal Directory Permissions](https://user-images.githubusercontent.com/4206926/73562458-77bfe980-445b-11ea-9041-86b6c6bd71c3.jpg)

### v6

On version **v6**, since we use Microsoft Graph, when running Scout with Service Principals the following [Microsoft Graph applications permissions](https://docs.microsoft.com/en-us/graph/permissions-reference) are required:

- `Directory.Read.All`
- `Policy.Read.All`

The following screenshot shows the required configuration:
![Screen Shot 2021-04-19 at 3 42 31 PM](https://user-images.githubusercontent.com/23067852/115295831-30894b80-a128-11eb-83c8-66de42d2391b.png)


## Options

### Subscriptions

- By default, Scout will query the subscriptions to which the provided credentials have access to, and use the first one in the list.
  - For some modes of authentication (i.e. Service Principal, or user credentials via Browser, the tenant ID must be provided).
- The `--subscriptions` option can be used to scan a number of subscriptions in one execution.
  - e.g. `--subscriptions 11111111-2222-3333-4444-555555555555 66666666-7777-8888-9999-000000000000`
- The `--all-subscriptions` option can be used to scan all the subscriptions to which the provided credentials have access.