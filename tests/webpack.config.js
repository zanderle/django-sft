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
