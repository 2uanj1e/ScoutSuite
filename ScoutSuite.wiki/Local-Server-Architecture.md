> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

# [v6] Local Server Architecture

The local server is used to feed report data to the frontend using a Flask server implementation. It used a traditional API structure with multiple endpoints returning specific information based on the parameters specified in the request.

All code related to the local server can be found in `ScoutSuite/core/server.py`.
The start_api function is called by the main.py with the report file and an exceptions file (if it exists).
The server only starts when this function is called.

## API Documentation

The API documentation can be consulted by:
1. Starting the local server with a report (using the `--server-only` argument (View `https://github.com/nccgroup/ScoutSuite/wiki/Using-the-new-V6-alpha-version` to check how to start the local server)
2. Visiting `http://localhost:5000/api-docs`

The documentation has been implemented using [flask-restx](https://flask-restx.readthedocs.io/en/latest/index.html).
In the default namespace, the details of every endpoint are documented with a short description and parameters (in-path and query parameters) information. It is possible to try out a specific route by clicking on the `Try it out` button.

## Debugging

If you are making changes in the API related code and would like to see the debugging information of the local server's activities, please comment out the following code in the start_api function:
```
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
```

This code is used to suppress all messages displayed by Flask.

## Endpoints

All API endpoints' path start with `/api` to distinguish frontend routing and calls to the API.
The base path `http://localhost:5000` returns the entry point (index.html) of the frontend code.
All tentative to connect to a non defined path returns a 404 error code if the path starts with a `/api` (eg. http://localhost:5000/api/superman) and returns the entry point of the frontend (index.html) if it doesn't start with `/api` (eg. http://localhost:5000/superman).