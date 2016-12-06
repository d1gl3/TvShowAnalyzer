var express = require('express');
var expressValidator = require('express-validator');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var Router = require('./routes/index');
var db = require("./src/db_connection.js");
var db_functions = require("./src/database");

var app = express();

var db_host = "localhost",
    db_port = "27017";


if (process.argv[2]) {
    console.log("DB Name: " + process.argv[2]);
    var db_name = process.argv[2];

    if (process.argv[3]) {
        console.log("DB Host: " + process.argv[3]);
        db_host = process.argv[3];

        if (process.argv[4]) {
            console.log("DB Port: " + process.argv[4]);
            db_port = process.argv[4];
        }
    }
} else {
    console.log("Missing Parameter Database Name. Please pass as first argument when starting the node server!")
    process.exit()
}

var db_connection_string = "mongodb://" + db_host + ":" + db_port + "/" + db_name;
console.log("Connection String: " + db_connection_string);

var db_fs = db_functions(db_connection_string);
var router = Router(db_connection_string, db_name, db_fs);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));
app.use(expressValidator({
    customValidators: {
        isInt: function(value) {
            return  value === parseInt(value, 10)
        },
        isStr: function (value) {
            return typeof value === 'string'
        }
    }
})); // this line must be immediately after express.bodyParser()!
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', router.router);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

module.exports = app;
