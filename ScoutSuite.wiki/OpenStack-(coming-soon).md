# OpenStack   <img src="https://object-storage-ca-ymq-1.vexxhost.net/swift/v1/6e4619c416ff4bd19e1c087f27a43eea/www-images-prod/openstack-logo/OpenStack-Logo-Mark.png" width="4%"></img>

## Authentication

**NOTE: ScoutSuite leverages [OpenstackSDK](https://docs.openstack.org/openstacksdk/latest/) to handle authentication; in particular it uses the `Connection` class as described [here](https://docs.openstack.org/openstacksdk/latest/user/connection.html).
Terms used in this section refer to [official OpenStack documentation](https://docs.openstack.org/keystone/latest/admin/identity-concepts.html).**

There are two ways to authenticate against an OpenStack instance.

### 1.  Using keyword arguments  
With this method the necessary parameters are passed as arguments to ScoutSuite.

Flag for authentication method: `--keywords`.  
Flags for authentication parameters:
-  `--auth_url` API endpoint to which ScoutSuite should authenticate;
-  `--username` username of the account;
-  `--user_domain_name` name of the domain to which belongs the account;
-  `--password` password for the account;
-  `--project_name` name of the project to work on;
-  `--project_domain_name` name of the domain to which belongs the project.

**NOTE: To generate a [project-scoped](https://docs.openstack.org/keystone/pike/admin/identity-tokens.html) token and consequently a project-scoped connection, all of the above arguments are required.**

### 2.  Configuration file: clouds.yaml
This method uses clouds.yaml, a configuration file commonly used in controller nodes to manage Openstack  instances.
Flag for authentication method: `--clouds_yaml`.  
If the configuration file is not in the working directory of ScotSuite, `--config_path` flag can be used to set its path. 

**NOTE: Please look [here](https://docs.openstack.org/os-client-config/latest/user/configuration.html#config-files) for more information on configuration file and its creation.**
## Examples
Project-scoped connection with `--keywords` flag
```sh
$ python scout.py os --keywords --username john --user_domain_name dom1 --password $3kr3t --project_name proj1 --project_domain_name dom1
```
Connection with `--clouds_yaml` flag
```sh
$ python scout.py os --clouds_yaml --cloud_name cloudTest --config_path <PATH/TO/CLOUDS.YAML>
```

