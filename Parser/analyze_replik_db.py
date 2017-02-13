#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import sys

import keywords as k
from MongoDB.MongoDBConnection import MongoDBConnection
from Parser.models.Episode import Episode
from Parser.models.Scene import Scene
from Parser.models.Season import Season
from Parser.models.Speaker import Speaker
from Parser.models.TvShow import TvShow
from Parser.utils import count_words_from_string

db = sys.argv[1]

mongo_db = MongoDBConnection()
season_coll = mongo_db.get_coll_by_db_and_name(db, k.SEASON_COLLECTION)
scene_coll = mongo_db.get_coll_by_db_and_name(db, k.SCENE_COLLECTION)
episode_coll = mongo_db.get_coll_by_db_and_name(db, k.EPISODE_COLLECTION)
replik_coll = mongo_db.get_coll_by_db_and_name(db, k.REPLIK_COLLECTION)
speaker_coll = mongo_db.get_coll_by_db_and_name(db, k.SPEAKER_COLLECTION)
tv_show_coll = mongo_db.get_coll_by_db_and_name(db, k.TV_SHOW_COLLECTION)
transkript_coll = mongo_db.get_coll_by_db_and_name(db, k.TRANSKRIPT_COLLECTION)


def log(string):
    print "### " + string


# Calculation of the scene stats
def calculate_scene_stats():
    log("Start Calculation Of Scene Stats")

    scenes = scene_coll.find({})

    scenes = list(scenes)

    for old_scene in scenes:

        scene = Scene()

        _id = old_scene.get("_id")
        _scene_number = old_scene.get("scene_number")
        _season_number = old_scene.get("season_number")
        _episode_number = old_scene.get("episode_number")

        log("Calculate Stats for Season %s Episode %s Scene %s" % (_season_number, _episode_number, _scene_number))

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

        log("Calculate Stats for Season %s Episode %s" % (_season_number, _episode_number))

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
            if not scene.get(k.NUMBER_OF_REPLICAS):
                continue

            updated_episode.add_scene(scene)

            scene_speakers = scene[k.SPEAKERS]

            for speaker in scene_speakers:
                updated_episode.add_speaker(speaker)

        updated_episode.calculate_replica_statistics()
        updated_episode.calculate_speaker_statistics()
        updated_episode.calculate_configuration_matrix()
        updated_episode.calculate_configuration_density()
        updated_episode.calculate_speaker_relations()
        updated_episode.calculate_force_related_graph_for_speakers()
        updated_episode.calculate_hamming_strings_for_speakers()

        updated_episode.calculate_speaker_probabilities([updated_episode.get_json()])

        # Update Episode data in MongoDB
        episode_coll.update({'_id': _id}, updated_episode.get_json())


def calculate_season_stats():
    log("Start Calculation Of Season Stats")
    seasons = season_coll.find({})

    for old_season in seasons:
        _id = old_season['_id']

        updated_season = Season()
        updated_season._season_number = old_season[k.SEASON_NUMBER]

        log("Calculate Stats for Season %s" % updated_season.season_number)

        episodes = episode_coll.find({k.SEASON_NUMBER: updated_season.season_number})

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
        episodes = episode_coll.find({k.SEASON_NUMBER: old_season[k.SEASON_NUMBER]})
        updated_season.calculate_force_related_graph_for_speakers(episodes)

        updated_season.calculate_hamming_strings_for_speakers()

        episodes = episode_coll.find({k.SEASON_NUMBER: old_season[k.SEASON_NUMBER]})
        updated_season.calculate_speaker_probabilities(list(episodes))

        season_coll.update({'_id': _id}, updated_season.get_json())


def calculate_tv_show_stats():
    log("Start Calculation Of Tv Show Stats")
    seasons = season_coll.find({})

    tv_show = TvShow("the_big_bang_theory")

    for season in seasons:
        tv_show.add_season(season)
        season_speakers = season[k.SPEAKERS]

        for speaker in season_speakers:
            tv_show.add_speaker(speaker)

    replics = replik_coll.find({})

    replik_length_list = {}

    for rep in replics:
        if "_%s" % rep.get(k.WORD_COUNT) not in replik_length_list:
            replik_length_list["_%s" % rep[k.WORD_COUNT]] = 1
        else:
            replik_length_list["_%s" % rep[k.WORD_COUNT]] += 1

    tv_show._replicasLength_List = replik_length_list

    tv_show.calculate_replica_statistics()
    tv_show.calculate_speaker_statistics()
    tv_show.calculate_configuration_matrix()
    tv_show.calculate_configuration_density()
    tv_show.calculate_speaker_relations()
    episodes = episode_coll.find({})
    tv_show.calculate_force_related_graph_for_speakers(episodes)
    tv_show.calculate_hamming_strings_for_speakers()

    tv_show = tv_show.get_json()

    speakers = tv_show[k.SPEAKERS]
    del tv_show[k.SPEAKERS]
    tv_show[k.NUMBER_OF_SPEAKERS] = len(speakers)

    tv_show_coll.insert(tv_show)

    for speaker in speakers:
        speaker["_id"] = speaker["name"]
        speaker_coll.insert(speaker)


def store_speakers_as_separate_objects():
    tv_show = tv_show_coll.find_one({})
    speakers = tv_show.get(k.SPEAKERS)

    for speaker in speakers:
        speaker["_id"] = speaker["name"]

        speaker_coll.insert(speaker)


def calculate_speaker_word_lists():
    speakers_cursor = speaker_coll.find({})

    speakers = [speaker for speaker in speakers_cursor]

    speaker_names = [speaker[k.NAME] for speaker in speakers]

    for speaker in speakers:
        name = speaker[k.NAME]
        string = ""

        repliks = replik_coll.find({'speaker': name})

        for replik in repliks:
            string += replik['replik']

        speaker_words, positive_words, negative_words, names, dist_word_count, noun_count, adverb_count, adjective_count, verb_count = count_words_from_string(
            string, speaker_names)

        speaker_words['list'].sort(key=lambda row: row[1], reverse=True)
        positive_words['list'].sort(key=lambda row: row[1], reverse=True)
        negative_words['list'].sort(key=lambda row: row[1], reverse=True)
        names['list'].sort(key=lambda row: row[1], reverse=True)

        speaker_top_100_dict_list = []

        for i in range(min([100, len(speaker_words["list"])])):
            word = speaker_words["list"][i]

            speaker_top_100_dict_list.append({
                "text": word[0],
                "weight": word[1]
            })

        speaker_top_100_pos_dict_list = []

        for i in range(min([100, len(positive_words["list"])])):
            word = positive_words["list"][i]

            speaker_top_100_pos_dict_list.append({
                "text": word[0],
                "weight": word[1]
            })

        speaker_top_100_neg_dict_list = []

        for i in range(min([100, len(negative_words["list"])])):
            word = negative_words["list"][i]

            speaker_top_100_neg_dict_list.append({
                "text": word[0],
                "weight": word[1]
            })

        speaker_top_5_name_dict_list = []

        for i in range(min([5, len(names["list"])])):
            name = names["list"][i]

            speaker_top_100_neg_dict_list.append({
                "text": name[0],
                "weight": name[1]
            })

        speaker['word_cloud_data'] = speaker_top_100_dict_list
        speaker['negative_words_cloud'] = speaker_top_100_neg_dict_list
        speaker['positive_words_cloud'] = speaker_top_100_pos_dict_list
        speaker['names_called'] = speaker_top_5_name_dict_list
        speaker['dist_word_count'] = dist_word_count
        speaker['noun_count'] = noun_count
        speaker['verb_count'] = verb_count
        speaker['adverb_count'] = adverb_count
        speaker['adjective_count'] = adjective_count

        if speaker_words["count"] != 0:
            speaker['negative_words_percentage'] = negative_words["count"] / float(speaker_words["count"])
            speaker['positive_words_percentage'] = positive_words["count"] / float(speaker_words["count"])

        if speaker.get('negative_words_percentage') and speaker.get('positive_words_percentage'):
            speaker['words_pos_ratio'] = float(speaker['positive_words_percentage']) / (
                float(speaker['negative_words_percentage']) + speaker['positive_words_percentage'])
            speaker['words_neg_ratio'] = float(speaker['negative_words_percentage']) / (
                float(speaker['negative_words_percentage']) + speaker['positive_words_percentage'])

        speaker["_id"] = speaker["name"]

        speaker_coll.update({'_id': speaker["name"]}, speaker)


def extract_speaker_hamming_distances():
    speakers_cursor = speaker_coll.find({})
    speakers = [speaker for speaker in speakers_cursor]

    for speaker in speakers:
        speaker_dists = {
            'show_hamming_dist': speaker[k.HAMMING_STRING]
        }

        for season_number in xrange(1, 9):
            season = season_coll.find_one({'season_number': season_number})
            season_speaker = next((item for item in season[k.SPEAKERS] if item[k.NAME] == speaker[k.NAME]), {})

            speaker_dists['season_%s' % season_number] = {
                'season_hamming_dist': season_speaker.get(k.HAMMING_STRING, "0" * int(season[k.NUMBER_OF_EPISODES]))
            }

            for episode_number in xrange(1, season[k.NUMBER_OF_EPISODES]):
                episode = episode_coll.find_one({'season_number': season_number,
                                                 'episode_number': episode_number})
                episode_speaker = next((item for item in episode[k.SPEAKERS] if item[k.NAME] == speaker[k.NAME]), {})

                speaker_dists['season_%s' % season_number]['episode_%s' % episode_number] = {
                    'episode_hamming_dist': episode_speaker.get(k.HAMMING_STRING,
                                                                "0" * int(episode[k.NUMBER_OF_SCENES]))
                }

        speaker[k.HAMMING_DISTANCES] = speaker_dists

        speaker_coll.update({'_id': speaker["name"]}, speaker)


def add_episode_titles():
    episodes = episode_coll.find({})

    for epi in episodes:
        transkript = transkript_coll.find_one({"season_number": epi[k.SEASON_NUMBER], "episode_number": epi[k.EPISODE_NUMBER]})

        epi[k.TITLE] = transkript[k.TITLE]

        episode_coll.update({'_id': epi['_id']}, epi)


if __name__ == "__main__":
    print "successfully invoked script"
    calculate_scene_stats()
    calculate_episode_stats()
    calculate_season_stats()
    calculate_tv_show_stats()
    #store_speakers_as_separate_objects()
    #  takes longer, execute separately
    calculate_speaker_word_lists()
    extract_speaker_hamming_distances()
    #add_episode_titles()
