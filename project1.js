var express = require("express"),
  app = express(),
  formidable = require('formidable'),
  util = require('util'),
  fs = require('fs-extra'),
  qt = require('quickthumb');


// Use quickthumb
app.use(qt.static(__dirname + '/'));

app.set('views', './'); //views files
app.set('view engine', 'jade'); //set templete

app.post('/upload', function(req, res) {
  var form = new formidable.IncomingForm();
  form.parse(req, function(err, fields, files) {
    if (files.upload1.name) {
      var pic11 = true;
    }
    if (files.upload2.name) {
      var pic22 = true;
    }
    if (files.upload3.name) {
      var pic33 = true;
    }
    res.render('uploadpage', {
      pic1: pic11,
      pic2: pic22,
      pic3: pic33,
      name: fields.title,
      source1: files.upload1.name,
      source2: files.upload2.name,
      source3: files.upload3.name
    }
    )
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path0 = this.openedFiles[0].path;
    var temp_path1 = this.openedFiles[1].path;
    var temp_path2 = this.openedFiles[2].path;
    /* The file name of the uploaded file */
    var file_name0 = this.openedFiles[0].name;
    var file_name1 = this.openedFiles[1].name;
    var file_name2 = this.openedFiles[2].name;
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path0, new_location + file_name0, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("0success!" + file_name0)
        // Handling get request
        console.log("Before put")

        updateDir();
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


  });
});

function updateDir() {
  var request = require('request');

  request({
    uri: "http://localhost:5000/images/input?task=" + "/upload",
    method: "PUT",
    timeout: 10000,
    followRedirect: true,
    maxRedirects: 10
  }, function(error, response, body) {
    console.log(body);
  });
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
