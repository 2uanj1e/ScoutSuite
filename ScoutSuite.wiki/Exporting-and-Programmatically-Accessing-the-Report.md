# Introduction

Being able to export the tool's finding into arbitrary format that may be consumed by other tools, or used to populate internal tracking system, is a feature that has been requested on many occasions and proved useful many times. This wiki page documents how Scout Suite's data is stored and how it may be exported to other formats.

# 1. Data location and format

After a Scout Suite run completes, all the necessary data is stored in a JavaScript file that is included by the HTML report. This file is located under `ScoutSuite/scoutsuite-report/scoutsuite-results/scoutsuite_results_<report name>.js`.

This JavaScript file is formatted as follow:

* The first line contains the variable definition code, necessary 
* Lines 2 through EOF contain a JSON-formatted object that contains all the data used by the HTML report, _i.e._ report metadata, cloud configuration, and analysis results.

```js
scoutsuite_results = 
{VALID_JSON_PAYLOAD}
```

Therefore, the entire data set may be used by discarding the file's first line. The following demonstrates several ways in which the data may be programmatically accessed using various common tools.

# 2. Use in Python

The following code snippet illustrates how one may load the Scout Suite data in a Python script (assuming that `file` is the path of the JSON report:

```python
import json

with open(file) as f:
    json_payload = f.readlines()
    json_payload.pop(0)
    json_payload = ''.join(json_payload)
    json_file = json.loads(json_payload)
    return json_file
```

# 3. Use with jq

Pretty-print the entire Scout Suite data:

```sh
$ tail /ScoutSuite/scoutsuite-report/scoutsuite-results/scoutsuite_results-<report name>.js -n +2 | jq '.'
```

Pretty-print a list of all security groups:

```sh
$ tail /ScoutSuite/scoutsuite-report/scoutsuite-results/scoutsuite_results-<report name>.js -n +2 | jq '.services.ec2.regions[].vpcs[].security_groups[]'
```
