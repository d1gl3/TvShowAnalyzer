/**
 * Created by paullichtenberger on 22.09.16.
 */

var Collection = require("./collections");
var db_con = require("./db_connection");
var hf = require("../src/helper_functions");

module.exports = function (db_connection_string) {

    var coll = null;

    db = db_con.connect(db_connection_string, function (err, db) {
        if (err) {
            console.log('Unable to connect to Mongo.');
            process.exit(-1);
        } else {
            coll = Collection(db);
        }
    });


    module.post_replik = function (req, res, callback) {
        //hf.validateReplik(req);

        data_list = req.body;
        var error_list = [];
        var success_list = [];

        for (var el in data_list) {
            if (data_list.hasOwnProperty(el)){

                var data = data_list[el];
                data._id = data.season_number + "_" + data.episode_number + "_" + data.scene_number + "_" + data.replik_number;

                // check for errors!
                var errors = req.validationErrors();
                if (errors) {
                    error_list.append(errors);
                    continue;
                }

                // insert scene, season, episode in database if they not exist

                var season = {
                    _id: "season_" + data.season_number,
                    season_number: data.season_number
                };
                coll.getSeasonCollection().insert(season, function (err) {
                    if (err) {
                        console.log("Season " + data.season_number + " already exists");
                    }
                });

                var episode = {
                    _id: "episode_" + data.season_number + "_" + data.episode_number,
                    season_number: data.season_number,
                    episode_number: data.episode_number
                };
                
                coll.getEpisodeCollection().insert(episode, function (err) {
                    if (err) {
                        console.log("Episode " + data.season_number + " already exists");
                    }
                });

                var scene = {
                    _id: "scene_" + data.season_number + "_" + data.episode_number + "_" + data.scene_number,
                    season_number: data.season_number,
                    episode_number: data.episode_number,
                    scene_number: data.scene_number
                };

                coll.getSceneCollection().insert(scene, function (err) {
                    if (err) {
                        console.log("Scene " + data.scene_number + " already exists");
                    }
                });

                // insert replik in database

                coll.getReplikCollection().insert(data, function (err, obj) {
                    if (err) {
                        error_list.push(err);
                    }
                });
            }
        }
        if (error_list) {
            res.statusCode = 400;
            callback(error_list, null, res);
        }
        else {
            res.statusCode = 200;
            callback(null, success_list, res);
        }
    };

    module.get_tv_show_stats = function (req, res, callback) {
        coll.getTVCollection().findOne({'name': 'the_big_bang_theory'}, function (err, doc) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, doc, res);
            }
        });
    };

    module.get_all_speakers = function (req, res, callback) {
        coll.getSpeakerCollection().find({}).toArray(function (err, docs) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, docs, res);
            }
        });
    };

    module.get_all_seasons = function (req, res, callback) {
        coll.getSeasonCollection().find({}).toArray(function (err, docs) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, docs, res);
            }
        });
    };

    module.get_all_episodes = function (req, res, callback) {
        coll.getEpisodeCollection().find({}).toArray(function (err, docs) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, docs, res);
            }
        });
    };

    module.get_all_speakers = function (req, res, callback) {
        coll.getSpeakerCollection().find({}).toArray(function (err, docs) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, docs, res);
            }
        });
    };

    module.find_speaker_by_name = function (req, res, callback) {

        var name = req.params.name;

        coll.getSpeakerCollection().findOne({"name": name}, function (err, doc) {
            if (err) {
                res.statusCode = 400;
                callback(err, null, res);
            }
            else {
                res.statusCode = 200;
                callback(null, doc, res);
            }
        });
    };

    return module;
};