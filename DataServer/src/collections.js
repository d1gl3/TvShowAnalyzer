require("mongodb");

module.exports = function (db) {

    var _db = db;

    module.getReplikCollection = function () {
        return _db.collection('replik_collection');
    };

    module.getSceneCollection = function () {
        return _db.collection('scene_collection');
    };

    module.getEpisodeCollection = function () {
        return _db.collection('episode_collection');
    };

    module.getSeasonCollection = function () {
        return _db.collection('season_collection');
    };

    module.getTVCollection = function () {
        return _db.collection('tv_show_collection');
    };

    module.getSpeakerCollection = function () {
        return _db.collection('speaker_collection');
    };

    return module;
};
