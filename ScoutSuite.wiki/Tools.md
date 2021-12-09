This section documents [tools](https://github.com/nccgroup/ScoutSuite/blob/master/tools/README.md) which help contribute to the project.

## process_raw_response.py

The [process_raw_response.py](https://github.com/nccgroup/ScoutSuite/blob/master/tools/process_raw_response.py) script helps automate a large part of the parsing/rendering of resources. You provide to the script a raw object as fetched by a facade, and it will parse the raw object and generate a valid partial. Once that's done, all you need to do (in simple scenarios) is tweak the parsing/partial to fit your needs. This removes a significant portion of manual labor.

To get a raw object, you can use a debugger. For example, using [PyCharm](https://www.jetbrains.com/pycharm/), you would set a breakpoint in the parsing function, and select `Copy Value` for the raw object:

![PyCharm Screenshot](https://user-images.githubusercontent.com/4206926/73474334-a15f0f00-438e-11ea-9d16-4cdfe18be136.png)

You could then pass the value to the script, also providing the provider, service and resource name:

```shell
$ python tools/process_raw_response.py -p azure -s aad -n user -v "{'additional_properties': {}, 'id': '/subscriptions[redacted]', 'name': '[redacted]', 'type': 'Microsoft.Authorization/roleAssignments', 'scope': '/subscriptions/[redacted]', 'role_definition_id': '/subscriptions/[redacted]', 'principal_id': '[redacted]', 'principal_type': 'User', 'can_delegate': None}"

user_dict = {}
user_dict['additional_properties'] = raw_user.additional_properties
user_dict['id'] = raw_user.id
user_dict['name'] = raw_user.name
user_dict['type'] = raw_user.type
user_dict['scope'] = raw_user.scope
user_dict['role_definition_id'] = raw_user.role_definition_id
user_dict['principal_id'] = raw_user.principal_id
user_dict['principal_type'] = raw_user.principal_type
user_dict['can_delegate'] = raw_user.can_delegate
return user_dict['id'], user_dict

<!-- aad users -->
<script id="services.aad.users.partial" type="text/x-handlebars-template">
    <div id="resource-name" class="list-group-item active">
        <h4 class="list-group-item-heading">{{name}}</h4>
    </div>
    <div class="list-group-item">
        <h4 class="list-group-item-heading">Information</h4>
        <div class="list-group-item-text item-margin">Additional Properties: <span id="aad.users.{{@key}}.additional_properties"><samp>{{value_or_none additional_properties}}</samp></span></div>
        <div class="list-group-item-text item-margin">Id: <span id="aad.users.{{@key}}.id"><samp>{{value_or_none id}}</samp></span></div>
        <div class="list-group-item-text item-margin">Name: <span id="aad.users.{{@key}}.name"><samp>{{value_or_none name}}</samp></span></div>
        <div class="list-group-item-text item-margin">Type: <span id="aad.users.{{@key}}.type"><samp>{{value_or_none type}}</samp></span></div>
        <div class="list-group-item-text item-margin">Scope: <span id="aad.users.{{@key}}.scope"><samp>{{value_or_none scope}}</samp></span></div>
        <div class="list-group-item-text item-margin">Role Definition Id: <span id="aad.users.{{@key}}.role_definition_id"><samp>{{value_or_none role_definition_id}}</samp></span></div>
        <div class="list-group-item-text item-margin">Principal Id: <span id="aad.users.{{@key}}.principal_id"><samp>{{value_or_none principal_id}}</samp></span></div>
        <div class="list-group-item-text item-margin">Principal Type: <span id="aad.users.{{@key}}.principal_type"><samp>{{value_or_none principal_type}}</samp></span></div>
        <div class="list-group-item-text item-margin">Can Delegate: <span id="aad.users.{{@key}}.can_delegate"><samp>{{value_or_none can_delegate}}</samp></span></div>
    </div>
</script>

<script>
    Handlebars.registerPartial("services.aad.users", $("#services\\.aad\\.users\\.partial").html());
</script>

<!-- Single aad user template -->
<script id="single_aad_user-template" type="text/x-handlebars-template">
    {{> modal-template template='services.aad.users'}}
</script>
<script>
    var single_aad_user_template = Handlebars.compile($("#single_aad_user-template").html());
</script>
```

Taking the example above, the first part of the output would be written into the `_parse_user` method, and the second one into the `services.aad.users.html` partial.

In a number of cases, the resource in question will have a parent node. This is the case of resources within AWS VPCs, Azure Subscriptions, etc. In these cases, you can pass the value with the optional `-a` parameter, and the additional node will be included in the partial's paths.

e.g.:

```shell
$ python tools/process_raw_response.py -p azure -s appservice -n web_app -a subscriptions -v "{[redacted]}"
```

### GCP 

GCP protobuf responses cannot be directly passed on to the script. The easiest way to get a valid value is to use the below example code, set a breakpoint and copy the value of `value`:

```python
def _parse_uptime_check(self, raw_uptime_check):

    from google.protobuf.json_format import MessageToJson
    value = MessageToJson(message=raw_uptime_check,
                          preserving_proto_field_name=True)
```

This can then be passed on to the script.
