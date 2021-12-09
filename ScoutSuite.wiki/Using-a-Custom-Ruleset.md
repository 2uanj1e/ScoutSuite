# Introduction

Scout Suite provides a default set of rules that the authors have chosen to be the best compromise between breadth of coverage and a minimum number of false positives. While this default ruleset provides many insights into the configuration of AWS, GCP and Azure environments, using a custom ruleset will provide significantly improved value. We strongly recommend frequent users of the tool generate their own set of rules.

# Step 1: Clone an existing ruleset
Cloning an existing ruleset is recommended to provide you with the base structure needed for the addition or subtraction of rules.

![image](https://user-images.githubusercontent.com/17322874/53530504-05fa5580-3abe-11e9-8e53-69ff54e8d994.png)

# Step 2: Enable / Disable rules

You can enable or disable rules by giving the value of `true` or `false`, respectively, to the field `"enabled":`. A rule with this value set to to `false` will not appear in any of the dashboards and subsequently you won't be able to click on it to have the culprit highlighted, however the data may still be available if you navigate to the proper page of the report. 

# Step 3: Modify the level associated with the rule

For each rule, the level (_i.e._ warning or danger) may be specified by entering either warning or danger next to the field `"level":`. This field affects the coloration of the triggered findings in order to signify varying levels of importance to the user reading the report.

![sc_2020-05-28_13h00m18s](https://user-images.githubusercontent.com/4206926/83133491-41ca0380-a0e3-11ea-935a-dab915cc8180.png)

### Configure parameterized rules

Some rules require parameters, which provides the following advantages:

1. A rule definition may be referenced multiple times in the ruleset, with only its arguments' values changing.
2. Rules that require environment-specific values, such as IP addresses or security group IDs are defined identically for any Scout Suite user.

The screenshot below illustrates how a parameterized rule typically looks like in the json file.

In this example, the rule takes two arguments:

1. The friendly/display name for the type of instances; in this case, "beefy".
2. The list of EC2 instance types considered as "beefy", each value separated by a comma.

![image](https://user-images.githubusercontent.com/17322874/53531439-3b547280-3ac1-11e9-9ed8-f831164714de.png)

# Step 4: Run Scout Suite using the new ruleset

With the new ruleset created, you may use pass it to Scout Suite using the `--ruleset` command line argument, as illustrated below.

```sh
$ scout aws --ruleset myruleset.json
```

If you already fetched the data and just wish to tweak the results, you may run a local analysis of the previously downloaded configuration using the `--local` argument.

```sh
$ scout aws --local --ruleset myruleset.json
```