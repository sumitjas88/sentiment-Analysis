var express = require('express');
var morgan  = require('morgan');
var bodyParser = require('body-parser');
var app = express();
var python;
app.use(morgan('dev'));
app.use(bodyParser());
var engine = require('consolidate');
app.set('views', __dirname);
app.engine('html', engine.mustache);
app.set('view engine', 'html');
app.use(express.static(__dirname + '/public'));
app.disable('etag');
//app.use(app.routes());
app.get('/analyticMonk/getTweets', function(req, res){
  var param = req.query.id;
  if(param){
    python = require('child_process').spawn(
     'python',
     ["jsonread.py"
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
       res.setHeader('Content-Type', 'application/json');
       res.send(200,output);
     });
   }else{
  res.send('Bad Request Please contact Administrator');
  }
});

app.get('/analyticMonk',function(req,res){
		res.render('Codeathon/index.html');
});
app.get('/analysis',function(req,res){
		res.render('Codeathon/analysis.html');
});


require('http').createServer(app).listen(3000, function(){
  console.log('Listening on 3000');
});
