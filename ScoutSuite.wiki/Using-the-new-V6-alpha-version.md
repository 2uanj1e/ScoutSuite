# Using the new V6 alpha version

⚠️ This document and the [v6-alpha](https://github.com/nccgroup/ScoutSuite/tree/v6-alpha/ScoutSuite) branch are a WIP. 

## Getting started

### 1. Install ScoutSuite

Start by install ScoutSuite locally [via Git](https://github.com/nccgroup/ScoutSuite/wiki/Setup#via-git).

### 2. Change to the v6-alpha branch

```
git checkout v6-alpha
```

## Starting the new server

In the base directory, run the following command to generate a report and start the server:

```
python scout.py PROVIDER
```
where `PROVIDER` can be `aws`, `azure` or `gcp`. 

If you already have a JSON report, you can use the following command to start the server without creating a new report.

```
python scout.py PROVIDER --server-only PATH_TO_JSON_REPORT_FILE.json
```

The JSON file is generated when creating a report and is located in the `scoutsuite-report` directory. 

You can now access the new web report at `http://localhost:5000`.

It is also possible to generate a report without starting the local server by using the report-only argument.
```
python scout.py PROVIDER --report-only
```

## FAQ 

### Can I use my old reports?

In the V6 version, we now generate `.json` files instead of `.js` files. If you need to use an old `.js` report, all you have to do is open the file, remove the first line and change the file extension from `.js` to `.json`. The content of the reports hasn't change but some old IDs are not supported in the new frontend.

## Know issues

This branch is currently a WIP. It should be stable, but some parts of the report could still have un-identified issues. We are planning a beta release on April 20th.  