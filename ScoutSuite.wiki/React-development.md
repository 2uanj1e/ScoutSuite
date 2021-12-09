> ⚠️ Warning: This is WIP - See [this PR](https://github.com/nccgroup/ScoutSuite/pull/1290) for details.

## Requirements

You need to have a Node.JS environment (version 10 or above) installed on your local machine. See the Node.JS website for more information: <https://nodejs.org/en/>

## Installing dependencies

Make sure you are in the `ScoutSuite/frontend` directory then run: 

```
npm install
```

## Starting the React development server

Make sure you are in the `ScoutSuite/frontend` directory then run: 

```
npm start
```

The command will automatically open a tab at `http://localhost:3000`. The React development server supports hot reloading so your changes will appear automatically. 

You will also need to have the local web server running on port 5000.

## Fix linting issue

If a linting issue is detected, the React won't compile the app. To fix command mistakes automatically, you can use the following command.  

Make sure you are in the `ScoutSuite/frontend` directory then run: 
```
npm run lint
```

If some issues can't be automatically fixed, make sure to manually fix them. PRs when merging to the `develop` branch will fail if there are errors with the linting. 