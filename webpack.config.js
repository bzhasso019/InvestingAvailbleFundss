const path = require('path');

module.exports = {
  entry: './app/static/js/aaa.js',
  output: {
    path: path.resolve(__dirname, 'app/static/dist'),
    filename: 'bundle.js',
  },
  mode: 'development'
};