var express = require('express');
var morgan  = require('morgan');
var bodyParser = require('body-parser');
var app = express();
var hackariba;
app.use(morgan('dev'));
app.use(bodyParser());
//app.use(app.routes());
app.get('/analyticMonk/getTweets', function(req, res){
  var param = req.query.id;
  if(param){
   var python = require('child_process').spawn(
     'python',
     ["twitterstream.py"
     , param]
     );
     var output = "";
   console.log(param);
   python.stdout.on('data', function(data){ output += data });
   console.log(output);
     python.on('close', function(code){ 
       if (code !== 0) {  
           return res.send(500, code); 
       }
       return res.send(200, output);
     }); 
  }else{
  res.send('Bad Request Please contact Administrator');
  }
});

require('http').createServer(app).listen(3000, function(){
  hackariba = require('child_process').spawn(
     'python',
     ["jsonread.py"]
     );
   var output = "";
   python.stdout.on('data', function(data){ output += data });
   console.log(output);
  console.log('Listening on 3000');
});