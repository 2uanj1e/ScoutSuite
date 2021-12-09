# Scout Suite Rules

Scout Suite rules use a recursive engine and a battery of test cases, which means no Python or coding skills are necessary to create or modify a rule; however, understanding of Scout Suite's data structure may be necessary if you're starting from scratch.

The following rule, found in `ScoutSuite/providers/azure/rules/findings/appservice-http-2-disabled.json`, is a good example: 

```json
{
    "description": "HTTP 2.0 Disabled",
    "rationale": "Periodically, newer versions are released for HTTP either due to security flaws or to include additional functionality. Using the latest HTTP version for web apps to take advantage of security fixes, if any, and/or new functionalities of the newer version.<br><br>Newer versions may contain security enhancements and additional functionality. Using the latest version is recommended in order to take advantage of enhancements and new capabilities. With each software installation, organizations need to determine if a given update meets their requirements and also verify the compatibility and support provided for any additional software against the update revision that is selected.<br><br>HTTP 2.0 has additional performance improvements on the head-of-line blocking problem of old HTTP version, header compression, and prioritization of requests. HTTP 2.0 no longer supports HTTP 1.1's chunked transfer encoding mechanism, as it provides its own, more efficient, mechanisms for data streaming.",
    "remediation": "Using Console:<ol><li>Login to Azure Portal using https://portal.azure.com</li><li>Go to \"App Services\"</li><li>Click on each App</li><li>Under \"Setting\" section, Click on \"Application settings\"</li><li>Ensure that \"HTTP Version\" set to \"2.0\" version under \"General settings\"</li></ol>",
    "compliance": [
        {
            "name": "CIS Microsoft Azure Foundations",
            "version": "1.1.0",
            "reference": "9.10"
        }
    ],
    "references": [
        "https://docs.microsoft.com/en-us/azure/app-service/web-sites-configure#general-settings"
    ],
    "dashboard_name": "Web Apps",
    "path": "appservice.subscriptions.id.web_apps.id",
    "conditions": [
        "and",
        [
            "appservice.subscriptions.id.web_apps.id.http_2_enabled",
            "false",
            ""
        ]
    ],
    "id_suffix": "http_2_enabled"
}
```

The https://github.com/nccgroup/ScoutSuite/blob/master/tools/format_findings.py tool can be leveraged to properly format rules.

# Rule Attributes

The following is a complete list of rule attributes that may be defined in the JSON rule definition:

* `description` (required): A brief description of the rule, displayed on the service's dashboard. This field allows HTML formatting.
* `rationale`: An explanation of why the rule matters, displayed when clicking on the `+` icon in the service dashboard. This field allows HTML formatting.
* `remediation`: Content regarding issue remediation. This field allows HTML formatting.
* `compliance`: A list of objects explaining which compliance measure, version, and reference point to look towards to understand.
* `references`: A list (`[]`) of URL links to reference documents for this finding.
* `dashboard_name` (required): The human-friendly name of the resources that are checked, displayed on the service's dashboard.
* `display_path`: The path to the parent resource that must be displayed when inspecting the rule's results. This is useful when the `path` the rule applies to differs. If this value is not provided, clicking on the finding will default to the value defined in `path.
* `path` (required): The path to the resources for which the rule applies. `id` is used when iteration over all items in a list or dictionary should be applied. Defines the resources that will be displayed when clicking on a finding in the dashboard.
* `conditions` (required): A list of conditions that, if met, will result in the resource to be flagged.
* `key`: Legacy field from the HTML ruleset generator
* `keys`: Legacy field from the HTML ruleset generator
* `arg_names`: Legacy field from the HTML ruleset generator
* `id_suffix`: If a custom HTML view has been created, this is used to enable color highlighting based on HTML IDs.
* `class_suffix`: If a custom HTML view has been created, this is used to enable color highlighting based on HTML classes.

# Minimal Rule Definition

All rules are defined under `ScoutSuite/providers/<provider>/rules/findings/`. The following snippet is the entire definition of the AWS `User without MFA` rule (`ScoutSuite/providers/aws/rules/findings/iam-user-without-mfa.json`). Let's have a look at the various values that are defined to make it work:

* description: A brief description of the rule, displayed on the service's dashboard.
* path: The path to the resources for which the rule applies. `id` is used when iteration over all items in a list or dictionary should be applied.
* dashboard_name: The human-friendly name of the resources that are checked, displayed on the service's dashboard.
* conditions: A list of conditions that, if met, will result in the resource to be flagged.
* id_suffix: If a custom HTML view has been created, this is used to enable color highlighting.

```json
{
    "description": "User without MFA",
    "dashboard_name": "Users",
    "path": "iam.users.id",
    "conditions": [
        "and",
        [
            "iam.users.id.",
            "withKey",
            "LoginProfile"
        ],
        [
            "iam.users.id.MFADevices",
            "empty",
            ""
        ]
    ],
    "keys": [
        "iam.users.id.name"
    ],
    "id_suffix": "mfa_enabled"
}
```

At the very least, these five attributes must be set when creating a new rule for Scout Suite. 

## dashboard_name

The `Users` value is displayed in the browser:

![dashboard_name](https://user-images.githubusercontent.com/4206926/78562172-41b33300-7819-11ea-966f-b1c337fa1f4c.jpg)

## id_suffix

The `mfa_enabled` value is set in the `ScoutSuite/output/data/html/partials/aws/services.iam.users.html` HTML partial which defines how the IAM users are displayed in the report:

```html
  <!-- IAM user partial -->
  <script id="services.iam.users.partial" type="text/x-handlebars-template">
    <div id="resource-name" class="list-group-item active">
      <h4 class="list-group-item-heading">{{name}}</h4>
    </div>
    <div class="list-group-item">
      <h4 class="list-group-item-heading">Information</h4>
      <div class="list-group-item-text item-margin">Creation date: {{CreateDate}}</div>
    </div>
    <div class="list-group-item">
      ...
      <p class="list-group-item-text item-margin">Multi-Factor enabled: <span id="iam.users.{{id}}.mfa_enabled">{{has_mfa? MFADevices}}</span></p>
...
```

This value is also set in the rule's `id_suffix` field, making it highlighted in the report:

![id_suffix](https://user-images.githubusercontent.com/4206926/78562246-598ab700-7819-11ea-86ee-8c704d8b0aca.jpg)

# Conditions Formatting

As mentioned above, the `conditions` attribute is a list of conditions that must be met in order for the processing engine to flag the resource as a finding. 

The basic format of a condition expression is as follow:

1. The first element may be string that declares the logical operation that must be performed when combining each condition's result when multiple conditions are necessary; its value must be one of "and" or "or".

1. Any other element must be a list of 3 items:
   1. The path to the value to be tested
   1. The test case to be used (provided by opinel)
   1. The value to be tested against

If a rule can be summarized by a single condition, it may be defined as follow:

```json
 "conditions" = [ "path_to_value_1", "equal", "trigger_value_1" ]
```

If multiple conditions are necessary, then the format would look as follow:

```json
"conditions" = [
    "and",
    [ "path_to_value_1", "equal", "trigger_value_1" ],
    [ "path_to_value_2", "equal", "trigger_value_2" ]
]
```

Note that conditions may be nested, so a more complex rule may look like the following:

```json
"conditions" = [
    "and",
    [ "path_to_value_1", "equal", "trigger_value_1" ],
    [ "path_to_value_2", "equal", "trigger_value_2" ],
    [
        "or",
        [ "path_to_value_3", "equal", "trigger_value_3" ],
        [ "path_to_value_4", "equal", "trigger_value_4" ]
    ]
]
```

All the implemented conditions can be found in https://github.com/nccgroup/ScoutSuite/blob/master/ScoutSuite/core/conditions.py.

## Reusing Conditions in Multiple Findings

To avoid code duplication, conditions that are used in multiple rules may be declared in standalone files and included in a rule. In this case, the definition of the rule's conditions would look as follow.

```json
"conditions" = [
    "and",
    [ "path_to_value_1", "equal", "trigger_value_1" ],
    [ "_INCLUDE_(conditions/condition-filename.json)", "", ""]
]
```

Where the files stored under `ScoutSuite/providers/<provider>/rules/conditions/condition-filename.json` contains the following payload:

```json
{
    "conditions": [ "path_to_value", "testCase", "test_value" ]
}
```

# Dynamic Values

## Passing Arguments

A list of arguments can be passed from rulesets to rules. For example, the `ScoutSuite/providers/aws/rules/rulesets/default.json` ruleset includes the following rule:

```json
"acm-certificate-with-close-expiration-date.json": [
    {
        "args": [
            "7"
        ],
        "enabled": true,
        "level": "warning"
    }
],
```

The `ScoutSuite/providers/aws/rules/findings/acm-certificate-with-close-expiration-date.json` rule is defined as follows:

```json
{
    "description": "ACM Certificate Expiring in Less Than _ARG_0_ Days",
    "rationale": "Ensure that certificates which are in use are not about to expire.",
    "dashboard_name": "Certificates",
    "path": "acm.regions.id.certificates.id",
    "conditions": [
        "and",
        [
            "acm.regions.id.certificates.id",
            "withKey",
            "NotAfter"
        ],
        [
            "acm.regions.id.certificates.id.NotAfter",
            "newerThan",
            [
                "_ARG_0_",
                "days"
            ]
        ]
    ],
    "id_suffix": "NotAfter"
}
```

As can be seen in the above, the value `7` is passed as the `_ARG_0_` value, and will be dynamically replaced during rule evaluation. Any number of arguments can be passed in this way (`_ARG_0_`, `_ARG_1_`, `_ARG_2_`, etc.)

## Dynamic Test Values

Sometimes, it can be necessary to perform tests against dynamic values. The `_GET_VALUE_AT_` macro can help to parameterize the rule at runtime. For example, the rule defined in `ScoutSuite/providers/aws/rules/findings/ec2-security-group-opens-all-ports-to-self.json`, which flags security groups that create a virtually flat network between all instances associated with the group, is defined as follow:

```json
{
    "description": "Unrestricted Network Traffic within Security Group",
    "dashboard_name": "Rules",
    "display_path": "ec2.regions.id.vpcs.id.security_groups.id",
    "path": "ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.security_groups.id",
    "conditions": [
        "and",
        [
            "_INCLUDE_(conditions/security-group-opens-all-ports.json)",
            "",
            ""
        ],
        [
            "ec2.regions.id.vpcs.id.security_groups.id.rules.id.protocols.id.ports.id.security_groups.id.GroupId",
            "equal",
            "_GET_VALUE_AT_(ec2.regions.id.vpcs.id.security_groups.id)"
        ]
    ]
}
```

Notice the use of the shared condition "security-group-opens-all-ports" in this rule. The second condition checks whether one of the security group grants authorizes an EC2 security group whose ID matches the source group ID. This is enabled by the use of `_GET_VALUE_AT_`

## Dynamic Source Values

Some rules may require knowledge of the ID associated with different type of resources and combine them in order to fetch the right test value. Similar to test values, the `_GET_VALUE_AT_` command may be used to provide a parameterized path to the source value at runtime. For example, matching EC2 instances with network ACL configuration can be challenging for the following reasons:

* Network ACLs are defined at a VPC level
* Network ACLs are associated at a subnet level
* EC2 instances inherit their subnet's ACLs

In order to create a rule or finding that flags EC2 instances whose subnet's NACLs are wide open, several calls to `_GET_VALUE_AT_` are necessary, as illustrated in the following snippet:

```json
{
    "conditions":
        [ "vpc.regions.id.vpcs.id.network_acls._GET_VALUE_AT_(vpc.regions.id.vpcs.id.subnets._GET_VALUE_AT_(ec2.regions.id.vpcs.id.instances.id.network_interfaces.id.SubnetId).network_acl).allow_all_ingress_traffic", "notEqual", "0" ]
}
```

This snippets illustrates that calls to `_GET_VALUE_AT_` may be nested. In such event, the processing engine resolves the deepest `_GET_VALUE_AT_`, then iterates back to the top until all values are resolved. In this example, values
would be resolved in this order:

1. The subnet ID associated with the network interface
2. The network ACL ID associated with the previously determined subnet ID

# Type of Rules

Scout Suite processes two rulesets at each run:

1. The findings ruleset, which is used to compute the data displayed on the
various dashboards. Unless a different ruleset is specified, the default ruleset
will be processed. A custom finding ruleset may be specified using the
`--ruleset` argument, as illustrated below:

```sh
$ scout --profile <profile> --ruleset ScoutSuite/providers/azure/rules/rulesets/cis-1.0.0.json
```

2. The filters ruleset, which is used to compute filter data on the various
resource-specific views. There is currently no option to specify a different
filter ruleset.

For more information about rulesets, refer to https://github.com/nccgroup/ScoutSuite/wiki/Using-a-Custom-Ruleset.
