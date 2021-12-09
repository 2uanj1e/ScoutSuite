# Table of contents
* [Introduction](#introduction)
* [Dependencies](#dependencies)
* [Structure](#structure)
* [Authentication strategy](#authentication-strategy)
* [Provider](#provider)
* [Services](#services)
* [Metadata](#metadata)
* [Facade](#facade)
* [What's next?](#whats-next)
* [Provider implementation checklist](#provider-implementation-checklist)

# Introduction
This guide describes the process of implementing support for a new provider. We worked really hard to streamline the process of implementing a provider. The thing is, Scout Suite is a big software. We decided it was better to keep some things explicit than abstracting too much. This means you're going to have to write a bit of code.

To demonstrate how one would go about implementing a new provider, we will implement a fictional provider called _Neat Services For the Web_ (NSFW).

# Dependencies
You are probably going to need to use some kind of library in order to communicate with the cloud provider you are integrating to Scout. That's fine, add the required dependencies to `requirements.txt`.

# Structure
Scout's codebase is separated into different providers. You will find most of the files related to _AWS_ under the `ScoutSuite/providers/aws` folder, for example. You can go ahead and create a folder for your new provider. In our case, we will create the `ScoutSuite/providers/nsfw` folder.

There are 4 important files you are going to need.
1. `autentication_strategy.py`
2. `provider.py`
3. `services.py`
4. `metadata.json`

In the following sections, we will dive deep into each of these files.

# Authentication strategy
The authentication strategy is a class that must, given some arguments, return credentials necessary to authenticate to the API client. It is used in the `run_scan` method.

This is what `authentication_strategy.py` should look like:
```py
class NSFWAuthenticationStrategy(AuthenticationStrategy):

    def authenticate(self, **kwargs):
        # You should get the credentials here and return them.
        return credentials
```

You also need to register your new authentication strategy in the `_strategies` dictionary found in the `providers\base\authentication_strategy_factory.py` file. Otherwise, you will get an `InvalidAuthenticationStrategyException`.


# Provider

TODO

# Services

The services file is where you register all your services, hence the name. For our provider, it will look something like this:

```py
class NSFWServicesConfig(BaseServicesConfig):

    def __init__(self, credentials: NSFWCredentials= None, **kwargs):
        super(NSFWServicesConfig, self).__init__(credentials)

        # This is where you would instantiate your provider's client library facade. You can then inject it into your services.
        facade = NSFWFacade(credentials)

        # Here, you register your services. The three following services are fictional.
        # By convention, the services should not call the provider client library directly,
        # they should instead go through a facade.
        self.sqldatabases = SQLDatabases(facade)
        self.nosqldatabases = NoSQLDatabases(facade)
        self.virtualmachines = VirtualMachines(facade)

    # This is used by the base class
    def _is_provider(self, provider_name):
        return provider_name == 'nsfw'

```

# Metadata

What Scout does is basically pulling data and putting it into a big data structure. It then generates an HTML report, so you can view the data structure in a nice format. The `metadata.json` file tells the UI what your data structure looks like, so it can display it.

For our provider, it would look like this:
```js
{
  // You can group similar services at this level. This will be reflected by one dropdown menu in the report.
  "databases": { 

     // This represents one service type. It is reflected by a sub-dropdown in the main dropdown menu.
    "sqldatabases": {

      // Those are the resources nested inside 
      "resources": {
        "databaseserver": {

          // _cols_ tells the UI how many columns it should display for this specific resource.
          // One column should be used for summaries, external surface attack reports, etc. 
          // Two columns should be used for most resource types. The left column displays a list of the instances
          // of this specific resource type, the right column shows the details of each instance.
          "cols": 2,
          // _path_ is the path of the resource in the data structure. This will be the handlebarsjs context (https://handlebarsjs.com/execution.html) of the page in the report.
          "path": "services.sqldatabase.databaseserver"
        },
        "snapshots": {
          "cols": 2,
          "path": "services.sqldatabase.snapshots"
        }
      },
      "nosqldatabases": {
        "resources": {
             // etc.
          }
        }
      }
    }
  },
  "cloudcomputing": {
    "virtualmachines": {
      // etc.
    }
  }
}
```

# Facade

The facade is where we encapsulate all the calls to the providers' client libraries. You will probably not need it at this point, but it might be a good idea to create the scaffolding. The facade is mostly used for resources fetching. We decided to add this layer to clearly separate the concerns: the resources files take care of the parsing and the facade takes care of the fetching. Learn more about it the [resources fetching system architecture guide](https://github.com/nccgroup/ScoutSuite/wiki/Resources-fetching-system-architecture#facade).

# What's next?
So now that we've implemented a provider, we can [implement services](https://github.com/nccgroup/ScoutSuite/wiki/Implementing-support-for-a-new-service) and [rules](https://github.com/nccgroup/ScoutSuite/wiki/HowTo:-Create-a-new-rule). We also expect you to update the wiki to document your provider.

# Provider implementation checklist
If you implement a new provider, you can use this checklist in your GitHub issue.

- Install the dependencies
- Implement `authentication_strategy.py`
- Implement `provider.py`
- Implement `services.py`
- Create `metadata.json`
- Add support for your provider in the CLI
- Implement UI elements if needed
- Write documentation
