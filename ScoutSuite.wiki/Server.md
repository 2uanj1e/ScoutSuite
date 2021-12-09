# Server
**This feature has been deprecated.**
## Security
PLEASE NOTE: Using this functionality as of now is insecure as it requires wide open CORS. An attacker could potentially use a page from a website he controls to exfiltrate the report data, even if it is not exposed.
## Use case
The traditional way use of Scout is to run the tool which will generate an local HTML report to be viewed. The problem with this approach is that when dealing with huge amount of data (over 400mb), the browser cannot load it all into RAM at once. In these cases, what we can do is serve the report result over a web server. 
## Current limitations
### Size
The current hard size limit for this is about 2Gb, as the underlying library to access the SQLite database doesn't support saving nested dictionaries yet and SQLite can only support up to 2GB of data in a single data blob. Note that these limits are still theoratical and haven't been tested.
## Usage
### Azure
To generate the report for azure, use a command simillar to this:
`./scout.py azure -c --result-format sqlite`
To server the report, use the following command:
`./scout.py azure -c --serve`
This will serve the report on 127.0.0.1:8000. Not that, for now, You still need to connect to the cloud provider to connect, but this can be fixed with a bit of refactoring.   
To serve a specific report:
`./scout.py azure -c --serve reportname`
To serve on a specific socket, you can use the following options:
`./scout.py azure -c --serve --host 0.0.0.0 --port 80`
Please note that this can only be used for testing the server for now, as the static report doesn't allow this for now.
### AWS
The same principles as with Azure apply for AWS, although you'll want to replace `azure -c` with `aws` or `aws AUTHENTICATION_METHOD`. For example : `aws --serve` would launch the server to read an AWS report saved with SQLite.
### GCP
The same principles as with Azure apply for GCP, although you'll want to replace `azure -c` with `gcp AUTHENTICATION_METHOD`. For example : `gcp --user-account --serve` would launch the server to read a GCP report saved with SQLite.

## Routes
Once you've launched the server you can read the data it projects manually in order to debug. The routes available can be viewed in `core/server.py` but here's an overview of the routes currently accessible :
- `http://127.0.0.1:8000/api/summary` : Returns all of the data excepted for the ones that scale up with the amount of resources. It allows the client to do a single request to fetch most of the information, afterwards we can use different routes for the data that increases with the size of an account.
- `http://127.0.0.1:8000/api/full?key=` : Returns everything in the object specified, or everything if no object is specified.
- `http://127.0.0.1:8000/api/data?key=` : Returns the type of the object specified and it's keys.
- `http://127.0.0.1:8000/api/page?pagesize=1&page=1&key=` : Returns a page of the specified resource, page size and index must be given, first page is at index 0.

When viewing an object of an object you must use separators between your keys, we've currently selected a symbol that no one seems to use '¤' although it could easily be changed.
Here's an example of a full length query on Azure, the separator being translated : 
`http://127.0.0.1:8000/api/page?pagesize=1&page=1&key=services%C2%A4network%C2%A4network_watchers`

## What's left
- Make the --serve argument a subparser. This will require some changes as, right now, we need the provider object to find the filenames, which requires to log in.
- Serve the html report too on the server. This is cleaner and would simplify a lot the host/port configuration.
- Fix SQLiteDict so it supports nested dictionnaries, which would allow reports to go up to 140TB in size.
- Test this with heavy load to make sure it works in the intended scenario.
~~~