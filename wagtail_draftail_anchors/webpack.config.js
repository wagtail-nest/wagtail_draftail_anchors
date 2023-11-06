
const path = require('path');

module.exports = {
    entry: path.resolve(__dirname, "./static_src/wagtaildraftailanchors/js/wagtail_draftail_anchor.js"),
    output: {
        path: path.resolve(__dirname, 'static/wagtaildraftailanchors/js/'),
        filename: 'wagtail-draftail-anchor.js',
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }
      ]
    },
  };