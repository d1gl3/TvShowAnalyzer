from ForeverDreamingParser import ForeverDreamingParser as Parser
from MongoDB.MongoDBConnection import MongoDBConnection
from TvShowModel import Season, Scene, Speaker, Episode, TvShow
import glob
import re
import keywords as k
from utils import *

mongo_db = MongoDBConnection()
seasons = []
episodes = []
season_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SEASON_COLLECTION)
scene_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SCENE_COLLECTION)
episode_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.EPISODE_COLLECTION)
replik_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.REPLIK_COLLECTION)
tv_show_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.TV_SHOW_COLLECTION)

def log(string):
    print "### " + string

def parse_big_bang_theory_raw_html_to_repliks():
    # Read paths of html files in download folder
    log("Open HTML Files")

    raw_html_files = glob.glob('data/*.html')  # ["data/raw_html_0.html"]
    for html in raw_html_files:
        with open(html, "r") as f:
            html = f.read()

            # Regex for extracting Season and Episode number
            re_season_episode = re.compile(r'[0-9]+x[0-9]+')

            season_number, episode_number = re.search(re_season_episode, html).group(0).split('x')
            if season_number.startswith('0'):
                season_number = int(season_number[1:])
            if episode_number.startswith('0'):
                episode_number = int(episode_number[1:])

            log("Parsing Season %s Episode %s" % (season_number, episode_number))

            # Create Season object in database
            if "season_%s" % season_number not in seasons:
                log("Season %s not in database. Created!" % season_number)
                seasons.append("season_%s" % season_number)
                season = Season()
                season._season_number = season_number
                season_coll.insert_one(season.get_json())

            # Create Episode object in database
            if "%sx%s" % (season_number, episode_number) not in episodes:
                log("Season %s Episode %s not in database. Created!" % (season_number, episode_number))
                episodes.append("%sx%s" % (season_number, episode_number))
                episode = Episode()
                episode._season_number = season_number
                episode._episode_number = episode_number
                episode_coll.insert_one(episode.get_json())

            # Parse Episode HTML, saves Repliks and Scenes to MongoDB
            try:
                parser = Parser(season_number, episode_number)
                parser.parse_html(html)
            except Exception, e:
                log("Could not parse Season %s Episode %s" % (season_number, episode_number))
                log("Reason: %s" % e.message)

            log("Succesfully parsed Season %s Episode %s" %(season_number, episode_number))


# Calculation of the scene stats
def calculate_scene_stats():
    log("Start Calculation Of Scene Stats")

    scenes = scene_coll.find({})

    scenes = list(scenes)

    for old_scene in scenes:

        scene = Scene()

        _id = old_scene["_id"]
        _scene_number = old_scene["scene_number"]
        _season_number = old_scene["season_number"]
        _episode_number = old_scene["episode_number"]

        log("Calculate Stats for Season %s Episode %s Scene %s" %(_season_number, _episode_number, _scene_number))

        scene._scene_number = _scene_number
        scene._season_number = _season_number
        scene._episode_number = _episode_number

        _speakers = {}

        # Find all replicas for this scene
        repliks = replik_coll.find(
            {
                "scene_number": _scene_number,
                "season_number": _season_number,
                "episode_number": _episode_number
            }
        )

        repliks = list(repliks)

        for replik in repliks:
            _replik_speaker = replik[k.SPEAKER]
            _replik_length = replik[k.WORD_COUNT]

            # Speaker appearing the first time in the scene => Create new Speaker
            if _replik_speaker not in _speakers:
                _speakers[_replik_speaker] = Speaker(_replik_speaker)

            # Add Replic to Speaker, this already recalculates mean, median etc. for this Speaker
            _speakers[_replik_speaker].add_replica(_scene_number, _episode_number, _season_number, _replik_length)

            # Add Replic to Scence, this already recalculates mean, median etc. for this Scene
            scene.add_replica(_replik_length)

        # Add Speakers to Scene and calculate some statistics
        scene._number_of_speakers = len(_speakers)
        for speaker, value in _speakers.iteritems():
            scene.add_speaker(value.get_json())

        scene.calculate_speaker_statistics()
        scene.calculate_replica_statistics()

        # Update Scene data in MongoDB
        scene_coll.update({'_id': _id}, scene.get_json())


def calculate_episode_stats():
    log("Start Calculation Of Episode Stats")
    episodes = episode_coll.find({})

    for old_episode in episodes:
        _id = old_episode['_id']

        updated_episode = Episode()
        _season_number = old_episode["season_number"]
        _episode_number = old_episode["episode_number"]

        log("Calculate Stats for Season %s Episode %s" %(_season_number, _episode_number))

        updated_episode._season_number = _season_number
        updated_episode._episode_number = _episode_number

        # Find all replicas for this scene
        scenes = scene_coll.find(
            {
                "season_number": _season_number,
                "episode_number": _episode_number
            }
        )

        scenes = list(scenes)

        for scene in scenes:
            updated_episode.add_scene(scene)

            scene_speakers = scene[k.SPEAKERS]

            for speaker in scene_speakers:
                updated_episode.add_speaker(speaker)

        updated_episode.calculate_replica_statistics()
        updated_episode.calculate_speaker_statistics()
        updated_episode.calculate_configuration_matrix()
        updated_episode.calculate_configuration_density()
        updated_episode.calculate_speaker_relations()

        # Update Episode data in MongoDB
        episode_coll.update({'_id': _id}, updated_episode.get_json())


def calculate_season_stats():
    log("Start Calculation Of Season Stats")
    seasons = season_coll.find({})

    for old_season in seasons:
        _id = old_season['_id']

        updated_season = Season()
        updated_season._season_number = old_season[k.SEASON_NUMBER]

        log("Calculate Stats for Season %s" % updated_season._season_number)

        episodes = episode_coll.find({k.SEASON_NUMBER: updated_season._season_number})

        for episode in episodes:
            updated_season.add_episode(episode)

            episode_speakers = episode[k.SPEAKERS]

            for speaker in episode_speakers:
                updated_season.add_speaker(speaker)

        updated_season.calculate_replica_statistics()
        updated_season.calculate_speaker_statistics()
        updated_season.calculate_configuration_matrix()
        updated_season.calculate_configuration_density()
        updated_season.calculate_speaker_relations()

        season_coll.update({'_id': _id}, updated_season.get_json())

def calculate_tv_show_stats():
    log("Start Calculation Of Tv Show Stats")
    seasons = season_coll.find({})

    tv_show = TvShow()

    for season in seasons:
        tv_show.add_season(season)
        season_speakers = season[k.SPEAKERS]

        for speaker in season_speakers:
            tv_show.add_speaker(speaker)

    tv_show.calculate_replica_statistics()
    tv_show.calculate_speaker_statistics()
    tv_show.calculate_configuration_matrix()
    tv_show.calculate_configuration_density()
    tv_show.calculate_speaker_relations()

    tv_show_coll.insert(tv_show.get_json())

def calculate_speaker_stats():
    pass


if __name__ == "__main__":
    #parse_big_bang_theory_raw_html_to_repliks()
    #calculate_scene_stats()
    #calculate_episode_stats()
    #calculate_season_stats()
    calculate_tv_show_stats()
