# Google Cloud Platform <img src="https://user-images.githubusercontent.com/17322874/55969978-bb3b3400-5c4c-11e9-9957-cd9811c20718.png" width="10%"></img>

## Authentication

There are two ways to authenticate Scout against a GCP Organization or Project.

1.  User Account
    1.  Configure the cloud shell to use the appropriate User Account credentials (`gcloud init` command to use a new
    account or `gcloud config set account <account>` to use an existing account)
    2.  Obtain access credentials to run Scout with: `gcloud auth application-default login`
    3.  Run Scout with the `--user-account` flag
2.  Service Account
    1.  Generate and download service account keys in JSON format
    (refer to <https://cloud.google.com/iam/docs/creating-managing-service-account-keys>)
    2.  Run Scout with the `--service-account` flag while providing the key file path

## Permissions

The following roles can be attached to the member used to run Scout in order to grant necessary permissions:

- `Viewer`
- `Security Reviewer`
- `Stackdriver Account Viewer`

## Execution

Using a computer already configured to use gcloud command-line tool, you may use Scout using the following command:

```sh
$ python scout.py gcp --user-account
```

To run Scout using Service Account keys, using the following command:

```sh
$ python scout.py gcp --service-account </PATH/TO/KEY_FILE.JSON>
```
    
By default, only the inferred default Project will be scanned.

To scan a GCP ...
- Organization, use the `--organization-id <ORGANIZATION ID>` argument
- Folder, use the `--folder-id <FOLDER ID>` argument.
- Project, use the `--project-id <PROJECT ID>` argument
- All projects that a user/service account has access to, use the `--all-projects` flags.