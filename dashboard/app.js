var express = require('express');
var app = express();

var socket = require('socket.io')

var path = require('path');


var favicon = require('serve-favicon');

var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var users = require('./routes/users');

// Socket.IO setup


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// uncomment after placing your favicon in /public
app.use(favicon(path.join(__dirname, 'public', 'images/favicon.ico')));

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', index);
app.use('/users', users);


// Configure routes

// GET method route
app.get('/update', function (req, res) {
    console.log('incoming get request! Broadcasting Socket Message. ');
    //sendMessage('Hello World!');
    io.emit('updateGraph', 'Hello World!');
    res.send('Message sent.');
});


/*

// POST method route
app.post('/', function (req, res) {
    res.send('POST request to the homepage')
});
*/


app.set('port', 3000);

// Define Server & Socket connections
var server = app.listen(app.get('port'), function() {
    console.log('Express server listening on port ' + server.address().port);
});

var io = socket(server);
io.on('connection', function(socket) {
    console.log('Made SOCKET.IO Connection with');
    console.log(socket.id);
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});




// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

