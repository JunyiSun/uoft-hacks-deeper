var express = require("express"),
  app = express(),
  formidable = require('formidable'),
  util = require('util'),
  fs = require('fs-extra'),
  qt = require('quickthumb');

var open = require('open')

// Use quickthumb
app.use(qt.static(__dirname + '/'));

app.set('views', './'); //views files
app.set('view engine', 'jade'); //set templete

globalFileName1 = ""
globalFileName2 = ""
globalFileName3 = ""
fieldTitle = ""

app.get('/result', function(req, res) {
  res.render('resultpage', {
    pic1: true,
    pic2: true,
    pic3: true,
    name: fieldTitle,
    source1: globalFileName1,
    source2: globalFileName2,
    source3: globalFileName3
  });
});
app.post('/upload', function(req, res) {
  var form = new formidable.IncomingForm();
  form.parse(req, function(err, fields, files) {
    fieldTitle = fields.title
    if (files.upload1.name) {
      var pic11 = true;
      globalFileName1 = 'input1.jpg';
    }
    if (files.upload2.name) {
      var pic22 = true;
      globalFileName2 = 'input2.jpg';
    }
    if (files.upload3.name) {
      var pic33 = true;
      globalFileName3 = 'input3.jpg';
    }
    res.render('uploadpage', {
      pic1: pic11,
      pic2: pic22,
      pic3: pic33,
      name: fields.title,
      source1: globalFileName1,
      source2: globalFileName2,
      source3: globalFileName3
    }
    )
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path0 = this.openedFiles[0].path;
    var temp_path1 = this.openedFiles[1].path;
    var temp_path2 = this.openedFiles[2].path;
    /* The file name of the uploaded file */
    var file_name0 = 'input1.jpg';
    var file_name1 = 'input2.jpg';
    var file_name2 = 'input3.jpg';
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path0, new_location + file_name0, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("0success!" + file_name0)
        // Handling get request
        console.log("Before put request sent")
      }
    });
    fs.copy(temp_path1, new_location + file_name1, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("1success!" + file_name1)
      }
    });
    fs.copy(temp_path2, new_location + file_name2, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("2success!" + file_name2)
      }
    });
    updateDir();
  // request object executes here.
  });
});

function updateDir() {
  var request = require('request');
  // create a request object
  request({
    uri: "http://localhost:5000/images/input?task=" + "uploads",
    method: "PUT",
    timeout: 3000000,
    followRedirect: true,
    maxRedirects: 10
  }, function(error, body) {
    console.log(body);
    console.log("bla");
    open("http://localhost:8080/result")
  });
// request object executes at end of function
}

// Show the upload form
app.get('/', function(req, res) {
  res.render('uploadpage', {
    pic1: false,
    pic2: false,
    pic3: false
  })
});
app.listen(8080);
console.log("Server is running on port 8080.");
