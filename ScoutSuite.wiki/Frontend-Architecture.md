> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

# [v6] Frontend Architecture

The web report (frontend) is completely decoupled from the json report. This means that all the components are designed to work with all the available providers. The frontend will change the rendering of the different components depending on the content that is provided by the local server. 

## File structure
The frontend follows the [Create React App](https://create-react-app.dev/docs/folder-structure/) folder structure. The complete file structure looks like this:

```text
ScoutSuite/frontend
├── README.md
├── node_modules
├── package.json
├── .gitignore
├── public
│   ├── favicon.ico
│   ├── index.html
│   └── manifest.json
└── src
    │   ├── Pages // Pages
    │   │   └── PageName1
    │   │	├── index.js
    │   │	└── style.scss
    │   ├── Components // Reusable components (but not partials)
    │   │   └── Component1
    │   │	├── index.js
    │   │	└── style.scss
    │   ├── partials // Partials 
    │   │   └── Partial1 // Could be AWS/GCP/Azure with subfolders
    │   │	├── index.js
    │   │	└── style.sass
    │   ├── API // All code related to the API
    │   │	└──  api.js
    │   └── utils
    │      └── ToolFolder 
    │    	└── index.js
    ├── App.scss
    ├── App.js // Contains the routing
    ├── index.css
    └── index.js // Entry point
```
All React component must be place in folder. The folder name should be the same as the React component and the folder should always have a `index.js` file and optionally a `style.scss` for styles unique to the component. 

## Routing

All the routing is defined in the `App.js` file. Each route is associated to page component is the `src/Pages` folder. 

## Dynamic Partial Loading

The React component for a partial is dynamically loaded at runtime. Webpack is configured to build all the files in the `src/partials` directory as independent components. This allows us to load a partial based on the path for a resource that is given by the local server.  

## Partial rendering

To make it as easy as possible to add new partials, we decided to make the complex logic of displaying a partial value hidden when only adding/or modifying a partial. 

When a dynamic partial is loaded, the corresponding content is fetched from the local server. The response is passed to the `<PartialWrapper />` component that create a React Context. The content in the response includes `item` (data to display) and `path_to_issues` (array of which key in data contains an issue). 

When a `<PartialValue />` component is defined inside a partial, we read the corresponding React Context to access the value. We also check to see if an error exists for the current key using the `path_to_issues` array. The error is then highlighted depending on its severity and a button is added to add it to the exception list. 

It is important to always use the `<PartialValue />` component when rendering value as this component also contains the logic to highlight a tab if one of the sub-components has an error. 

## Build pipeline

We should never build the app locally. The production version of the React app is automatically built when a push is created on the `develop` branch. The output files are located in the `ScoutSuite/web_report` folder.  