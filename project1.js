var express = require("express"),
  app = express(),
  formidable = require('formidable'),
  util = require('util'),
  fs = require('fs-extra'),
  qt = require('quickthumb');

var myJSON = require("JSON");
var open = require('open')

// Use quickthumb
app.use(qt.static(__dirname + '/'));

app.set('views', './'); //views files
app.set('view engine', 'jade'); //set templete

globalFileName1 = ""
globalFileName2 = ""
globalFileName3 = ""
globalFileName111 = ""
globalFileName222 = ""
globalFileName333 = ""
fieldTitle = ""
caption1 = "AI caption1";
caption2 = "AI caption2";
caption3 = "AI caption3";

app.get('/result', function(req, res) {
  res.render('resultpage', {
    pic1: true,
    pic2: true,
    pic3: true,
    name: fieldTitle,
    source1: globalFileName1,
    source2: globalFileName2,
    source3: globalFileName3,
    cap1: caption1,
    cap2: caption2,
    cap3: caption3
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
  }, function(error, response) {
    console.log('RESPONSE.BODY IS      .....:')
    baba = JSON.parse(JSON.stringify(response.body))
    console.log(baba)
    baba = baba.replace('[', '')
    console.log(baba)
    baba = baba.replace(']', '')
    console.log(baba)
    baba = baba.replace(/"/g, '')
    console.log(baba)
    after = baba.split(",")
    caption1 = after[0]
    caption2 = after[1]
    caption3 = after[2]
    console.log(after)
    open("http://localhost:8080/result")
  });
// request object executes at end of function
}

app.get('/wordvect', function(req, res) {
  res.render('try', {
    pic1: true,
    pic2: true,
    pic3: true,
    name: fieldTitle,
    source1: globalFileName111,
    source2: globalFileName222,
    source3: globalFileName333,
    cap1: caption1,
    cap2: caption2,
    cap3: caption3
  });
});


app.post('/upload2', function(req, res) {
  var form = new formidable.IncomingForm();
  form.parse(req, function(err, fields, files) {
    fieldTitle = fields.title
    if (files.upload111.name) {
      var pic11 = true;
      globalFileName111 = 'input111.jpg';
    }
    if (files.upload222.name) {
      var pic22 = true;
      globalFileName222 = 'input222.jpg';
    }
    if (files.upload333.name) {
      var pic33 = true;
      globalFileName333 = 'input333.jpg';
    }
    res.render('uploadpage', {
      pic111: pic11,
      pic222: pic22,
      pic333: pic33,
      name: fields.title,
      source111: globalFileName111,
      source222: globalFileName222,
      source333: globalFileName333
    }
    )
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path0 = this.openedFiles[0].path;
    var temp_path1 = this.openedFiles[1].path;
    var temp_path2 = this.openedFiles[2].path;
    /* The file name of the uploaded file */
    var file_name0 = 'input111.jpg';
    var file_name1 = 'input222.jpg';
    var file_name2 = 'input333.jpg';
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path0, new_location + file_name0, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("00000success!" + file_name0)
        // Handling get request
        console.log("Before put request sent")
      }
    });
    fs.copy(temp_path1, new_location + file_name1, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("111111success!" + file_name1)
      }
    });
    fs.copy(temp_path2, new_location + file_name2, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("2222222success!" + file_name2)
      }
    });
    updateDir2();
  // request object executes here.
  });
});

function updateDir2() {
  var request = require('request');
  // create a request object
  request({
    uri: "http://localhost:5000/images/input?task=" + "uploads",
    method: "PUT",
    timeout: 3000000,
    followRedirect: true,
    maxRedirects: 10
  }, function(error, response) {
    console.log('RESPONSE.BODY IS      .....:')
    // baba = JSON.parse(JSON.stringify(response.body))
    // console.log(baba)
    // baba = baba.replace('[', '')
    // console.log(baba)
    // baba = baba.replace(']', '')
    // console.log(baba)
    // baba = baba.replace(/"/g, '')
    // console.log(baba)
    // after = baba.split(",")
    // caption1 = after[0]
    // caption2 = after[1]
    // caption3 = after[2]
    // console.log(after)
    open("http://localhost:8080/wordvect")
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
