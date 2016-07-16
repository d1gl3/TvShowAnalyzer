from ForeverDreamingParser import ForeverDreamingParser as Parser
from MongoDB.MongoDBConnection import MongoDBConnection
from TvShowModel import Season, Scene, Speaker
import glob
import re
import keywords as k
from utils import *

mongo_db = MongoDBConnection()
seasons = []
season_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SEASON_COLLECTION)
scene_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SCENE_COLLECTION)
replik_coll = mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.REPLIK_COLLECTION)


def parse_big_bang_theory_raw_html_to_repliks():
    # Read paths of html files in download folder
    raw_html_files = glob.glob('data/*.html')
    for html in raw_html_files:
        with open(html, "r") as f:
            html = f.read()

            # Regex for extracting Season and Episode number
            re_season_episode = re.compile(r'[0-9]+x[0-9]+')

            season_number, episode_number = re.search(re_season_episode, html).group(0).split('x')
            season_number = int(season_number.strip('0'))
            episode_number = int(episode_number.strip('0'))

            # Create Season object in database
            if "season_%s" % season_number not in seasons:
                seasons.append("season_%s" % season_number)
                season = Season()
                season._season_number = season_number
                season_coll.insert_one(season.get_json())

            # Parse Episode HTML, saves Repliks and Scenes to MongoDB
            parser = Parser(season_number, episode_number)
            parser.parse_html(html)


# Calculation of the scene stats
def calculate_scene_stats():
    scenes = scene_coll.find({})

    for old_scene in scenes:

        scene = Scene()

        _id = old_scene["_id"]
        _scene_number = old_scene["scene_number"]
        _season_number = old_scene["season_number"]
        _episode_number = old_scene["episode_number"]

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
            _speakers[_replik_speaker].add_replica(_replik_length)

            # Add Replic to Scence, this already recalculates mean, median etc. for this Scene
            scene.add_replica(_replik_length)

        # Add Speakers to Scene and calculate some statistics
        scene._number_of_speakers = len(_speakers)
        for speaker, value in _speakers.iteritems():
            scene.add_speaker(value.get_json())

        scene.calculate_speaker_statistics()

        # Update Scene data in MongoDB
        scene_coll.update({'_id': _id}, scene.get_json())




if __name__ == "__main__":
    #parse_big_bang_theory_raw_html_to_repliks()
    calculate_scene_stats()
