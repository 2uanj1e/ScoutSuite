> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

# Complex Partial Rendering

In some case, the `<PartialValue />` component is not enough to render more complex data. 

## Objects as list 

The most commun "advanced" rendering is an object where key is the `id` and the content are the values:

```js
const obj = {
  "id1": {
    "name": "Test 1",
    "desc": "Test 1 description",
  },
  "id2": {
    "name": "Test 2",
    "desc": "Test 2 description",
  }
}
```

We can use the `Object.entries(obj)` Javascript fonction to convert it to an array. We will then get the following array: 

```json
[
  ["id1", {
    "name": "Test 1",
    "desc": "Test 1 description",
  }],
  ["id2", {
    "name": "Test 2",
    "desc": "Test 2 description",
  }]
]
```

It is now possible to use this array with the `<PartialValue />` component and the `renderList` helper function. 

### Example 1: Rendering only the name

```js
// Define a fonction to render a user
const renderUsers = users => {
  // Render a list
  return renderList(
    users, 
    '', 
    [key, values] => values.name // Only use the value
   );
};

const Groups = () => {
  return (
    <>
        <PartialValue
          label="Users"
          valuePath="users"
          renderValue={values => renderUsers(
             Object.entries(values) // Convert to a list
          )} />
    </>
  );
};
```

In this example, we create a function to render a list based on the converted object. We recommend using the "renderList" function as much as possible as it will take care of displaying "None" for an empty list. 

This solution only works if the error is located on "users", not on key in the user object. See the following example to handle this. 

### Example 2: Rendering the name and the description

```js
// Define a fonction to render a user
const renderUsers = users => {

  // Render the partial values for every user
  const renderUser = ([key, values]) => (
    <>
      <PartialValue
        label="Name"
        valuePath={`users.${key}.name`} // Define the path to the data
        renderValue={valueOrNone} />
      <PartialValue
        label="Description"
        valuePath={`users.${key}.desc`}
        renderValue={valueOrNone} />
    </>
  );
  return renderList(users, '', user => renderUser(user));
};

// Define PropTypes 
const propTypes = {
  data: PropTypes.object,
};

const Groups = props => {
  const { data } = props; // Read the data directly

  return (
    <>
        {renderUsers(
          Object.entries(data.users) // Convert to a list
        )}
    </>
  );
};

Groups.propTypes = propTypes;
```
In this example, for every user we render a `<Partialvalue />` instead of rendering a `<PartialValue />` for all the users. This makes is more flexible and we can handle more complex rendering of each value. For example, the value uses the formatter `valueOrNone` in this example. 

Every partial receives a `data` prop that contains the same data about the resource that is available via the `<PartialValue />` component. You can read directly some information from this object to allow React to go through the content. 

One improvement could be to use the `<PartialSection />` component to avoid repeating "complex" `valuePath`. 

```js
const renderUsers = users => {
  const renderUser = ([key, values]) => (
    <PartialSection path={`users.${key}`}> // Partial Section with the base path
      <PartialValue
        label="Name"
        valuePath="name" // Simplified path
        renderValue={valueOrNone} />
      <PartialValue
        label="Description"
        valuePath="desc"
        renderValue={valueOrNone} />
    </>
  );
  return renderList(users, '', user => renderUser(user));
};
```

## Resource Links

A very common complex rendering use case is to render a list of resource link. Most of the time we only receive a list of IDs but want the render the name.  

Our custom `useResources` hook allow to fetch the details for some resources based on the IDs of these resources. 

```js
// Render a list of links to the user resource page
const renderUsers = users => {
  const renderUserLink = user => (
    <ResourceLink
      service="aad"
      resource="users"
      id={user.id}
      name={user.name}
    />
  );
  return renderList(users, '', user => renderUserLink(user));
};

// Render a list of links to the roles resource page
const renderRoles = (roles, rolesList) => { // We pass an extra custom list of roles
  const renderRole = role => {
    // We extract some information from the custom list
    const { subscription_id } = rolesList.find(r => r.role_id === role.id);
    return (
      <span>
        <ResourceLink
          service="rbac"
          resource="roles"
          id={role.id}
          name={role.name}
        />{' '}
        (subscription {subscription_id}) // We display the addition data here
      </span>
    );
  };
  return renderList(roles, '', role => renderRole(role));
};

// Define PropTypes 
const propTypes = {
  data: PropTypes.object,
};

const Groups = props => {
  const { data } = props;

  // Get a list of users based on the IDs in `data.users`
  const { data: users } = useResources('aad', 'users', data.users);

  // Creates a list of roles. For performances reasons, useMemo will only run the function inside when `data.roles` changes
  const rolesList = useMemo(() => data.roles.map(r => r.role_id), [data.roles]);

  // Get a list of roles based on the IDs in `rolesList`
  const { data: roles } = useResources('rbac', 'roles', rolesList);

  return (
    <>
      <TabsMenu>
        <TabPane title="Members">
          {renderUsers(users)}
        </TabPane>

        <TabPane title="Role Assignments">
          {renderRoles(roles, item.roles)}
        </TabPane>
      </TabsMenu>
    </>
  );
};

Groups.propTypes = propTypes;
```


