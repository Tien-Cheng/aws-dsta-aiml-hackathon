// Entry point to Backend Server
// Run: node server.js

var app = require('./controller/app.js');
var port=8080;

var server = app.listen(port, function () {
    console.log('Web App Hosted at http://localhost:%s',port);
});
