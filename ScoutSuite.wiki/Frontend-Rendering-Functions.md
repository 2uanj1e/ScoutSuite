> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

# Documentation

The following "render functions" allow to render values in the `<PartialValue />` component. They can also be used directly when rendering [complex partials](https://github.com/nccgroup/ScoutSuite/wiki/Frontend:-Creating-complex-partials).

### `convertBoolToEnable`

Convert a boolean to enabled or disabled

 * **Parameters:** `value` — 
 * **Returns:** `string` — 

### `convertBoolToCheckmark`

Convert a boolean to a checkmark or x

 * **Parameters:** `value` — 
 * **Returns:** `string` — 

### `convertBoolToString`

Convert a boolean to a readable boolean

 * **Parameters:** `title` — 
 * **Returns:** `string` — 

### `convertValueOrNever`

Convert value to never if invalid

 * **Parameters:** `value` — 
 * **Returns:** `any|string` — 

### `convertListToChips`

Convert a list of value to a list of chips

 * **Parameters:** `list` — 
 * **Returns:** `array|string` — 

### `convertBoolToYesOrNo`

Convert a boolean to a 'yes' or 'no'

 * **Parameters:** `value` — 
 * **Returns:** `string` — 

### `valueOrNone`

Return the value or the string 'None' if it doesn't

 * **Parameters:** `value` — 
 * **Returns:** `any` — 

### `formatDate`

Format Date

 * **Parameters:** `time` — 
 * **Returns:** `string` — 

### `renderWithInnerHtml`

Render div with content set throught innerHTML

 * **Parameters:**
   * `innerHtml` — 
   * `props` — 
 * **Returns:** `HTMLDivElement` — 

### `renderList`

Render the items in an object as an unordered list

 * **Parameters:**
   * `resources` — 
   * `accessor` — 
 * **Returns:** `HTMLUListElement` — 

### `renderSecurityGroupLink`

Render a Security Group object as a link

 * **Parameters:** `securityGroup` — 
 * **Returns:** `ResourceLink` — 

### `renderPolicyLink`

Render a Policy id as a link

 * **Parameters:** `id` — 
 * **Returns:** `ResourceLink` — 

### `renderFlowlogLink`

Render a FlowLog id as a link

 * **Parameters:** `id` — 
 * **Returns:** `ResourceLink` — 

### `renderAwsTags`

Render tags in an unordered list

 * **Parameters:** `tags` — 
 * **Returns:** `HTMLUListElement` — 
