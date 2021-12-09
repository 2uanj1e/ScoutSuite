> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

Here is the documentation of the most used components when creating a new partial. All components are defined in `ScoutSuite/frontend/src/components`. You can look at the "propTypes" of a component to understand when data it accepts. 

# Components

## `<InformationsWrapper />`

It's a simple wrapper for one or multiple `<PartialValue />` in the information section of a partial. If a partial doesn't have any tabs, you shouldn't wrap `<PartialValue />` in `<InformationsWrapper />`. 

**Example**
```js
<InformationsWrapper>
{/* One or more partial values */}
</InformationsWrapper>
```

**Props**
- `children` One or more `<PartialValue />` (required)



## `<TabsMenu />`

Creates a tab menu. The only valid childrens are one or more `<TabPane />`. 

**Example**
```js
<TabsMenu>
  {/* One or more tab pane */}
  <TabPane title="Tab 1"></TabPane>
  <TabPane title="Tab 2"></TabPane>
</TabsMenu>
```

**Props**
- `children` One or more `<TabPane />` (required)


## `<TabPane />`

Creates a tab menu. The only valid childrens are one or more `<TabPane />`. 

**Example**
```js
<TabPane
  title="Tab 1"
  disabled={someCondtion == isTrue}
>
  {/* Tab content */}
</TabPane>
```

**Props**
- `title: string` Name of the tab (required)
- `disabled: bool` Disables a tab (usually when their is no content. 
- `children` Tab content (required)

## `<PartialValue />`

Creates a tab menu. The only valid childrens are one or more `<TabPane />`. 

**Example**
```js
<PartialValue
  label="Value Label"
  valuePath="path.to.value"
  errorPath="path.to.error"
  renderValue={valueRenderingFunction}
  value={customValue}
  separator
  inline
  className="fancy-style"
  tooltip
/>
```

**Props**
- `label: string` Label of the value (required)
- `valuePath: string` Path to the value. For nested objects, use `path.to.value` (required)
- `value: string` Overwrites the value at `valuePath` 
- `errorPath: string|array<string>` Path or paths to the error. For nested objects, use `path.to.error`
- `separator: string` Overwrite the separator between `label` and the value. Default is `:`.
- `renderValue` It takes a function to modify the rendering of the value. See [Rendering Functions](https://github.com/nccgroup/ScoutSuite/wiki/Frontend:-Rendering-Functions) for more information and available functions.
- `inline: bool` Indicates to display the value inline
- `className: string` Adds a className to the wrapper of the value
- `tooltip: boolean` Adds a tooltip around the value (only use when really needed)
- `basePathOverwrite: string` Overwrite the base path to the value. This is used for [Complex Partials](https://github.com/nccgroup/ScoutSuite/wiki/Frontend:-Creating-complex-partials)

## `<PartialSection />`

When some partial values are nested, for example the name value is located at `networks.xyz.subnets.0.name`, it can be useful to wrap multiple the some `<PartialValue />` in a `<PartialSection />`. 

Instead of writting:

```js
<>
  <PartialValue valuePath="networks.xyz.subnets.0.id" />
  <PartialValue valuePath="networks.xyz.subnets.0.name" />
</>
```
you can now write
```js
<PartialSection path="networks.xyz.subnets.0">
  <PartialValue valuePath="id" />
  <PartialValue valuePath="name" />
</PartialSection>
```

**Example**
```js
<PartialSection
  path="path.to.section"
>
  {/* Nested <PartialValue /> */}
</PartialSection>
```

**Props**
- `path: string` Path to object (required)
- `children` Nested <PartialValue /> (required)

## `<ResourceLink />`

This component should be used when linking to another resource. If the `name` prop isn't defined, it will get it from the server by using the id. 

**Example**
```js
<ResourceLink
  service="storage"
  resource="buckets"
  id="abc"
  name="Bucket Name"
  nameProps={{ renderData: (name) => valueOrNone(name) }}
/>
```

**Props**
- `service: string` Service for the resource (required)
- `resource: string` Resource type (required)
- `id: string` Id of the resource (required)
- `name: string` Overwrites the name in the link
- `nameProps: object` Additional props for the `<ResourceName />` component. 

## `<ResourceName />`

Fetches a name for a resource based on it's ID. 

**Example**
```js
<ResourceName
  service="storage"
  resource="buckets"
  id="abc"
  renderData={(name) => valueOrNone(name)}
/>
```

**Props**
- `service: string` Service for the resource (required)
- `resource: string` Resource type (required)
- `id: string` Id of the resource (required)
- `renderData: object` Function to change how the name is rendered.
