var express = require('express');
var router = express.Router();
var db_con = require('../src/db_connection');
var collections = require('../src/collections');
var assert = require("assert");
var util = require('util');
var PythonShell = require('python-shell');
var path = require('path');
var exec = require('child_process').exec;
var sys = require("util");
var cors = require("cors");

module.exports = function (db_connection_string, db_name, db_fs) {

    var coll = null;
    var database_functions = db_fs;

    response_handler = function (err, doc, res) {
        if (err) {
            res.send(util.inspect(err.message), 400);
        }else {
            res.send(doc);
        }
    };

    db = db_con.connect(db_connection_string, function (err, db) {
        if (err) {
            console.log('Unable to connect to Mongo.');
            process.exit(-1);
        } else {
            coll = collections(db);
        }
    });


    // use it before all route definitions
    router.use(cors({origin: '*'}));

    /* GET home page. */
    router.get('/', function (req, res) {
        res.render('index', {title: 'Express'});
    });

    router.post('/api/post_replik', function (req, res) {
        database_functions.post_replik(req, res, response_handler);
    });

    router.get('/api/tv_show', function (req, res) {
        database_functions.get_tv_show_stats(req, res, response_handler);
    });

    router.get('/api/analyze_data', function (req, res) {
        exec('PYTHONPATH='+ path.join(__dirname, '..', '..') +' python ' + path.join(__dirname, '..', '..','Parser', 'parse_big_bang_theory.py ' + db_name), {maxBuffer: 1024 * 2000});
    });

    router.get('/api/speakers', function (req, res) {
       database_functions.get_all_speakers(req, res, response_handler);
    });

    router.get('/api/speakers/:name', function (req, res) {
        database_functions.find_speaker_by_name(req, res, response_handler);
    });

    router.get('/api/episodes', function (req, res) {
        database_functions.get_all_episodes(req, res, response_handler);
    });

    router.get('/api/seasons', function (req, res) {
        database_functions.get_all_seasons(req, res, response_handler);
    });

    router.get('/api/speeches', function (req, res) {
        database_functions.get_speeches_by_speaker(req,res, response_handler);
    });

    module.router = router;

    return module;

};
