# Table of contents
* [Introduction](#introduction)
* [AWS](#aws)
* [Azure](#azure)
* [GCP](#gcp)

# Introduction
This guide describes the process of implementing support for a new service for Amazon Web Services (AWS), Azure and Google Cloud Platform (GCP).

**Note** that the [process_raw_response.py](https://github.com/nccgroup/ScoutSuite/wiki/Tools#process_raw_responsepy) script can help automate this task.

# AWS

For this example, we will implement the AWS Lambda service. 

## Setup 
* Create a `awslambda` folder under `providers\aws\resources\`
* Create a `awslambda.py` file under `providers\aws\facade\`

## Implementing the service

Implementing an AWS service is pretty straightforward.  A simple service (like AWS lambdas) usually consists of two classes: a child of `Regions`, and a child of `AWSResources`. Of course, it can get way more complex if the service contains multiple nested resources.

The `AWSResources` child class usually consists of two methods: an implementation of the `fetch_all` method, which does three things:
1. Fetch the resources through the facade
2. Parse the raw resources
3. Populate its internal dictionary with the parsed resources

and (at least) a `_parse_*` method that parses the fetched resources:

```py
class Functions(AWSResources):
    def __init__(self, facade, region):
        super(Functions, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        # (1) Fetching
        raw_functions = await self.facade.awslambda.get_functions(self.region)
        
        for raw_function in raw_functions:
            # (2) Parsing
            name, resource = self._parse_function(raw_function)
            
            # (3) Populating
            self[name] = resource

    def _parse_function(self, raw_function):
        raw_function['name'] = raw_function.pop('FunctionName')
        return (raw_function['name'], raw_function)
```

The `Regions` implementation is also pretty straightforward. 
1. Define the `_children` attribute. The tuples should have the following format: (<child_resource_class>, <child_name>)
2. Call the super constructor to provide the service name
3. You may want to override the fetch_all method if you need to do some processing, just make sure you call the super `fetch_all`

```py
class Lambdas(Regions):
    # (1) define the children
    _children = [
        (Functions, 'functions')
    ]
    
    def __init__(self, facade: AWSFacade):
        # (2) call the `super` init and provide the service call
        super(Lambdas, self).__init__('lambda', facade)
```

You might also need to implement methods in the facade `providers\aws\facade\awslambda.py` to fetch your data.

## Registering the service

The last step is registering the service. To do so, simply add it to the list of services in the `ScoutSuite\providers\aws\services.py` file in the `__init__` method. Please keep the services sorted in alphabetical order.

# Azure

For this example, we will implement the Azure Key Vault service. 

## Setup 
* Create a `keyvault` folder under `providers\azure\resources\`
* Create a `keyvault.py` file under `providers\azure\facade\`

## Implementing the service

Implementing an Azure service is pretty straightforward.  A simple service (like Azure Key Vault) usually consists of one single class that inherits from `AzureResources`. Of course, it can get way more complex if the service contains multiple nested resources (in that case, there could be multiple classes, some of them inheriting from `AzureCompositeResources` and others from `AzureResources`. You can check `ScoutSuite/providers/azure/resources/sqldatabase/` for a complex example.).

The `AzureResources` child class usually consists of two methods: an implementation of the `fetch_all` method, which does three things:
1. Fetch the resources through the facade
2. Parse the raw resources
3. Populate its internal dictionary with the parsed resources

and (at least) a `_parse_*` method that parses the fetched resources:
```py
class KeyVaults(AzureResources):
    async def fetch_all(self):
        self['vaults'] = {}
        # (1) Fetching
        for raw_vault in await self.facade.keyvault.get_key_vaults():
            # (2) Parsing
            id, vault = self._parse_key_vault(raw_vault)

            # (3) Populating
            self['vaults'][id] = vault

        self['vaults_count'] = len(self['vaults'])

    def _parse_key_vault(self, raw_vault):
        vault = {}
        vault['id'] = get_non_provider_id(raw_vault.id)
        vault['name'] = raw_vault.name

        return vault['id'], vault
```

You also need to implement methods in the facade `providers\azure\facade\keyvault.py` to fetch your data.

## Registering the service

The last step is registering the service. To do so, simply add it to the list of services in the `ScoutSuite\providers\azure\services.py` file in the `__init__` method. Please keep the services sorted in alphabetical order.

# GCP

For this example, we will implement the GCP Cloud Storage service. 

## Setup 
* Create a `cloudstorage` folder under `providers\gcp\resources\`
* Create a `cloudstorage.py` file under `providers\gcp\facade\`

## Implementing the service

The `Resources` child class usually consists of two methods: an implementation of the `fetch_all()` method and a parsing method (`_parse_resource_name()`). The `fetch_all()`method does three things:
1. Fetch the resources through the facade
2. Call the parsing method
3. Populate its internal dictionary with the parsed resources

and (at least) a `_parse_*` method that parses the fetched resources:
```py
class Buckets(Resources):
    def __init__(self, facade, project_id):
        super(Functions, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        # (1) Fetching
        raw_buckets = await self.facade.cloudstorage.get_buckets(self.project_id)
        
        for raw_bucket in raw_buckets:
            # (2) Parsing
            bucket_id, bucket = self._parse_bucket(raw_bucket)
            
            # (3) Populating
            self[bucket_id] = bucket

    def _parse_bucket(self, raw_bucket):
        bucket_dict = {}
        bucket_dict['id'] = get_non_provider_id(raw_bucket.id)
        bucket_dict['name'] = raw_bucket.name
        bucket_dict['creation_date'] = raw_bucket.time_created
        ...
        return bucket_dict['id'], bucket_dict
```

The `Projects` implementation is also pretty straightforward. 
1. Define the `_children` attribute. The tuples should have the following format: (<child_resource_class>, <child_name>)
2. You may want to override the fetch_all method if you need to do some processing, just make sure you call the super `fetch_all`

```py
class CloudStorage(Projects):
    # (1) define the children
    _children = [
        (Buckets, 'buckets')
    ]
```

You also need to implement methods in the facade `providers\gcp\facade\cloudstorage.py` to fetch your data.

## Registering the service

The last step is registering the service. To do so, simply add it to the list of services in the `ScoutSuite\providers\gcp\services.py` file in the `__init__` method. Please keep the services sorted in alphabetical order.

