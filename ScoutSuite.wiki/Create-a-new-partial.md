> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

# How to create a partial 

## What are partials?
In the Scout Suite Web Report, a "Partial" refers to the displayed information for a particular resource. For example, a AWS s3 Bucket is considered to be a resource and the partial would define the information to display for this resource. 

## Create a new partial

Creating a new partial is pretty straightforward but it's very important to understand how to name the partial and how to read to access the informations.

To make it as easy as possible, all the logic to access the information and highlight the errors is handled outside of the partial. You can read more about the web report architecture to learn how it works.   


***
 

### 1. How to name the partial?

This is the most important step. Partials are dynamically loaded (loaded at runtime) based on information given by the server. If the information doesn't match, the partial won't be loaded. 

The name is based on the path in the `metadata.json` file. For example, if we want to add a partial for AWS S3 Buckets, the path in the [metadata.json](https://github.com/nccgroup/ScoutSuite/blob/master/ScoutSuite/providers/aws/metadata.json) file is `services.s3.buckets`. To get the partial name, you need to _remove_ the `services.` and _add_ `.id` at the end. 

➡️ **The transformed (valid) name is `s3.buckets.id`.**

You need to create a folder with this name and an `index.js` file inside the directory of the provider located a `ScoutSuite/fontend/src/partials`. _Do not name the `.js` file directly!_ 


***


### 2. Creating a base partial

We suggest you start by using of the examples below depending on your needs. These basic examples should cover most of the use-cases. You can copy/paste the examples in the `index.js` file you create at the previous step.  

#### Information only partial 

```js
import React from 'react';

import { PartialValue } from '../../../components/Partial';

const PartialName = () => {
  return (
    <>
        <PartialValue
          label="Name"
          valuePath="name" />
        <PartialValue
          label="Name"
          valuePath="name" />
    </>
  );
};

export default PartialName;
```

#### Partial with tabs

```js
import React from 'react';

import { PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Tabs';
import { renderList } from '../../../utils/Partials/index';
import InformationsWrapper from '../../../components/InformationsWrapper';

const PartialName = () => {
  return (
    <>
      <InformationsWrapper>
        <PartialValue
          label="Name"
          valuePath="name" />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Tabe Name #1">
          <PartialValue
            label="Roles"
            valuePath="roles"
            renderValue={renderList} />
        </TabPane>
        <TabPane title="Tabe Name #2">
          <PartialValue
            label="User"
            valuePath="user" />
        </TabPane>
      </TabsMenu>
    </>
  );
};

export default PartialName;
```


***


### 3. Add a single value

```js
<PartialValue
  label="Name" // Required
  valuePath="name" // Required
  errorPath="name" // Optional
  renderValue={convertBoolToEnable} // Optional
/>
```

The `PartialValue` component is used to display a value. **DO NOT RENDER VALUES DIRECTLY.** The `PartialValue` component contains the logic of checking if a value has an error and adds the color highlighting and option to add to the exception list. 

The most commun props are:
- `label` Name of the value
- `valuePath` Path to the value to render. If it's a nested value, use the Javascript object syntax `path.to.value`.  
- `errorPath` If the error path is different than the value path. 
- `renderValue` It takes a function to modify the rendering of the value. See [Rendering Functions](https://github.com/nccgroup/ScoutSuite/wiki/Frontend:-Rendering-Functions) for more information and available functions. 

More props are available for more complexe use cases. See [React Frontend Components](https://github.com/nccgroup/ScoutSuite/wiki/Frontend-React-Components) for the complete documentation.

***


### 4. Add a list 

#### Simple list

For a _list of strings_, you can use the `renderList` function to render automatically the list as bullet points. 

```js
// Import before the component
import { renderList } from '../../../utils/Partials/index';

// In the component
<PartialValue
    label="Roles"
    valuePath="roles"
    renderValue={renderList} />
```

#### Converting objects to lists

Some of the list are returned as objects where the id is the key and the content is the values. Javascript has three useful built-in functions to convert objects to array depending on your needs:

- `Object.keys(obj)` Creates an array of keys
- `Object.values(obj)` Creates an array of values
- `Object.entries(obj)` Create an array of "tuples" (array with two values) in the following format [key, value]

Here is a small example: 
```js
const obj = { key1: { name: "Test1" }, key2: { name: "Test 2"}}

const keys = Object.keys(obj);
console.log(keys) // OUTPUTS: ["key1", "key2"]

const values = Object.values(obj);
console.log(values) // OUTPUTS: [{ name: "Test1" }, { name: "Test 2"}]

const entries = Object.entries(obj);
console.log(entries) // OUTPUTS: [["key1", { name: "Test1" }], ["key2", { name: "Test 2"}]]
```
#### Complex lists

If you need to render a list that isn't a list of strings, see the documentation on [Complex Partials](https://github.com/nccgroup/ScoutSuite/wiki/Frontend:-Creating-complex-partials).
