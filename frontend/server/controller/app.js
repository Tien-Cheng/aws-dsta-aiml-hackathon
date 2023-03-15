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
app.post('/text', upload.single("file"), function(req,res){
    console.log(req.body)

    // return res.status(200).send([{'description': req.body.text}]);
    return res.status(200).send([
      {
        "text": "Please do not add nonsense",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9998065829277039
          },
          {
            "Name": "toxic",
            "Score": 0.0001722178130876273
          },
          {
            "Name": "obscene",
            "Score": 0.00009582550410414115
          }
        ]
      },
      {
        "text": "to Wikipedia. Such edits are",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9997995495796204
          },
          {
            "Name": "toxic",
            "Score": 0.00017764008953236043
          },
          {
            "Name": "obscene",
            "Score": 0.00009818559919949621
          }
        ]
      },
      {
        "text": "considered vandalism and quickly undone.",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9998452663421631
          },
          {
            "Name": "toxic",
            "Score": 0.00014578818809241056
          },
          {
            "Name": "obscene",
            "Score": 0.00007812384137650952
          }
        ]
      },
      {
        "text": "If you would like to",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9991036057472229
          },
          {
            "Name": "toxic",
            "Score": 0.0007668289472348988
          },
          {
            "Name": "obscene",
            "Score": 0.0002614073164295405
          }
        ]
      },
      {
        "text": "experiment, please use the sandbox",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9998452663421631
          },
          {
            "Name": "toxic",
            "Score": 0.00014567076868843287
          },
          {
            "Name": "obscene",
            "Score": 0.00007835692667867988
          }
        ]
      },
      {
        "text": "instead. Thank you.",
        "classes": [
          {
            "Name": "non_hate",
            "Score": 0.9998413324356079
          },
          {
            "Name": "toxic",
            "Score": 0.00014589595957659185
          },
          {
            "Name": "obscene",
            "Score": 0.00008212903048843145
          }
        ]
      }
    ]);
});

app.post('/video', upload.single("file"), function(req,res){
  console.log(req.body)

  // return res.status(200).send([{'description': req.body.text}]);
  return res.status(200).send([
    {
      "text": "Please do not add nonsense",
      "classes": [
        {
          "Name": "non_hate",
          "Score": 0.9998065829277039
        },
        {
          "Name": "toxic",
          "Score": 0.0001722178130876273
        },
        {
          "Name": "obscene",
          "Score": 0.00009582550410414115
        }
      ]
    },
    {
      "text": "to Wikipedia. Such edits are",
      "classes": [
        {
          "Name": "non_hate",
          "Score": 0.9997995495796204
        },
        {
          "Name": "toxic",
          "Score": 0.00017764008953236043
        },
        {
          "Name": "obscene",
          "Score": 0.00009818559919949621
        }
      ]
    },
    {
      "text": "considered vandalism and quickly undone.",
      "classes": [
        {
          "Name": "non_hate",
          "Score": 0.9998452663421631
        },
        {
          "Name": "toxic",
          "Score": 0.00014578818809241056
        },
        {
          "Name": "obscene",
          "Score": 0.00007812384137650952
        }
      ]
    },
    {
      "text": "If you would like to",
      "classes": [
        {
          "Name": "non_hate",
          "Score": 0.9991036057472229
        },
        {
          "Name": "toxic",
          "Score": 0.0007668289472348988
        },
        {
          "Name": "obscene",
          "Score": 0.0002614073164295405
        }
      ]
    },
    {
      "text": "experiment, please use the sandbox",
      "classes": [
        {
          "Name": "non_hate",
          "Score": 0.9998452663421631
        },
        {
          "Name": "toxic",
          "Score": 0.00014567076868843287
        },
        {
          "Name": "obscene",
          "Score": 0.00007835692667867988
        }
      ]
    }
  ]);
});

// Catch all if none of the above endpoints match
app.all('*', function (req, res) {
    return res.sendStatus(400);
});

module.exports = app;