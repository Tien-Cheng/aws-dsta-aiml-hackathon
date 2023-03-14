// Routing for Endpoint APIs
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const multer = require('multer');

//Cross Origin to access both frontend and backend server
var cors = require("cors");
app.options('*',cors());
app.use(cors());

//MIDDLEWARE
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

/* FILE STORAGE */
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, "assets");
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname);
    },
});

const upload = multer({ storage });

/* ENDPOINTS */
app.post('/posts', upload.single("picture"), function(req,res){
    console.log(req.body)

    return res.status(200).send([{'description': req.body.description}]);
});

// Catch all if none of the above endpoints match
app.all('*', function (req, res) {
    return res.sendStatus(400);
});

module.exports = app;