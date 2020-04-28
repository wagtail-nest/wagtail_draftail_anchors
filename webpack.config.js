
const path = require('path');

module.exports = {
    entry: "./static_src/js/wagtail_draftail_anchor.js",
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
    output: {
        path: path.resolve(__dirname, 'static/js/'),
        filename: 'wagtail-draftail-anchor.js',
    }
  };