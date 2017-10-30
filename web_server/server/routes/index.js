let express = require('express');
let router = express.Router();
let path = require('path');

/* GET home page. */
// If you access the root directory, return index.html
router.get('/', function(req, res, next) {
  res.sendFile("index.html", { root: path.join(__dirname, '../../client/build')});
});

module.exports = router;
