## Example Project for django_sft

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Install the requirements for the package:

		pip install -r requirements.txt

2. Navigate to the root directory of your application (same as `manage.py`)
3. Make and apply migrations

		python manage.py makemigrations

		python manage.py migrate

4. Run the server

		python manage.py runserver

5. Access from the browser at `http://127.0.0.1:8000`


## Using django-sft with webpack

Since django-sft produces static files, you can process them further any way you like. You could use Django Pipeline,
or [Django webpack-loader](https://github.com/owais/django-webpack-loader).

Install the webpack-loader (and follow the instructions there). To make it work with django-sft, a few things
need to be added.

First, override the way `script` and `style` tags are added to the `html` template.

```python
GET_STYLE_TAG = lambda static_name: f"""{{% render_bundle '{static_name.replace('/sft', '').replace('/', '_')}' 'css' %}}"""
GET_SCRIPT_TAG = lambda static_name: f"""{{% render_bundle '{static_name.replace('/sft', '').replace('/', '_')}' 'js' %}}"""
```

These two functions take the `static_name` (which is the name django-sft will give to the resulting static files out of the SFT)
and return the right tags we want to inject.

In this example, we'll be using webpack-loader's `render_bundle` template tag to render the bundles created by webpack.
We need to somehow figure out what the bundle names will be. They could be anything, but for this example, we decided to
name the bundles like so:

```
/<app_name>/static/<app_name>/sft/<name> ---> <app_name>_<name>
```

We have to make sure that webpack will do the same. We can use a configuration like this:

```js
var path = require('path');
var glob = require('glob')
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const appNames = ["example"];
// Get all SFT files for the listed apps
const allSFTfiles = glob.sync(`@(${appNames.join(",")})/templates/**/*.sft`);

// Create sensible entry names (for webpack) out of those files
const entryNames = allSFTfiles.map((sftPath) => {
  const parts = path.parse(sftPath);
  const dirParts = parts.dir.split('/');
  const root = dirParts[0];
  const name = `${parts.dir.replace(`${root}/templates/`, '').split('/').join('_')}_${parts.name}`;
  // If SFT was found at <app_name>/templates/<app_name>/<file_name>.sft
  // We want to name the entry point <app_name>_<file_name>
  return { name, root, entryName: parts.name };
});

// Create the entry object for webpack
const entry = {};
entryNames.map(app => {
  // For each SFT file (found in entryNames) find associated static files
  const files = glob.sync(`${app.root}/static/**/sft/${app.entryName}.*`);
  // If any files found
  if (files.length) {
    // Put them under this entry point (and add relative path, so webpack knows how to resolve it)
    entry[app.name] = files.map(f => `./${f}`);
  }
});

module.exports = {
  mode: process.env.NODE_ENV,
  entry: entry,
  output: {
    filename: '[name].js',
    path: __dirname + '/static/dist/',
    publicPath: '/static/dist/',
  },
  module: {
    rules: [
      {
        test: /\.s?css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
    new BundleTracker({filename: './webpack-stats.json'})
  ]
};
```

We can now `manage.py runserver` and `npm start` (assuming it points to something like `webapck --watch`) in another terminal
tab, and now SFTs static files are processed and bundled with webpack. In this config we also enabled Sass for our styling.
Other than that this webpack config is quite basic and we could add a lot more to make it work for our example.
