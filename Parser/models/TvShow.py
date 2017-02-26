import itertools

import operator

from BaseModel import BaseModel
from copy import deepcopy
from Parser.utils import *
import keywords as k


class TvShow(BaseModel):
    def __init__(self, name):
        BaseModel.__init__(self)
        self._name = name

    def get_json(self):
        return {
            k.FORCE_DIRECTED_DATA: self._force_directed_data,
            k.NUMBER_OF_EPISODES: self._number_of_episodes,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.NUMBER_OF_SPEAKERS: self._number_of_speakers,
            k.NUMBER_OF_SEASONS: self._number_of_seasons,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.SPEAKERS: self._speakers,
            k.CONFIGURATION_MATRIX: self._configuration_matrix,
            k.CONFIGURATION_DENSITY: self._configuration_density,
            k.NAME: self._name
        }

    def calculate_speaker_statistics(self):
        speakers = deepcopy(self._speakers)
        new_speakers = []
        new_speakers_dict = {}

        for speaker in speakers:
            if speaker[k.NAME] not in new_speakers_dict:
                new_speakers_dict[speaker[k.NAME]] = speaker
            else:
                new_speakers_dict[speaker[k.NAME]][k.NUMBER_OF_REPLICAS] += speaker.get(k.NUMBER_OF_REPLICAS, 0)

                old_replica_length_list = new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_LIST]
                for key, v in speaker[k.REPLICAS_LENGTH_LIST].iteritems():
                    if key not in old_replica_length_list:
                        old_replica_length_list[key] = v
                    else:
                        old_replica_length_list[key] += v

                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_LIST] = old_replica_length_list
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_TOTAL] += speaker.get(k.REPLICAS_LENGTH_TOTAL, 0)

                old_appeared_in_seasons_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SEASONS]
                for season_number in speaker.get(k.APPEARED_IN_SEASONS, []):
                    if season_number not in old_appeared_in_seasons_list:
                        old_appeared_in_seasons_list.append(season_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SEASONS] = old_appeared_in_seasons_list

        speakers = [v for speaker, v in new_speakers_dict.iteritems()]

        for speaker in speakers:
            speaker[k.WORD_PERCENTAGE] = float(speaker[k.REPLICAS_LENGTH_TOTAL]) / float(
                self._replicasLength_total)
            speaker[k.REPLIK_PERCENTAGE] = float(speaker[k.NUMBER_OF_REPLICAS]) / float(self._number_of_replicas)

            if speaker[k.REPLICAS_LENGTH_LIST]:
                lengths = []
                for key, v in dict(speaker[k.REPLICAS_LENGTH_LIST]).iteritems():
                    key = key[1:]
                    for i in range(v):
                        lengths.append(int(key))
                speaker[k.REPLICAS_LENGTH_AVERAGE] = mean(lengths)
                speaker[k.REPLICAS_LENGTH_MEDIAN] = median(lengths)
                speaker[k.REPLICAS_LENGTH_MAX] = max(lengths)
                speaker[k.REPLICAS_LENGTH_MIN] = min(lengths)

            new_speakers.append(speaker)
        self._speakers = new_speakers

    def add_season(self, season):
        self._number_of_seasons += 1
        self._number_of_replicas += season[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += season[k.REPLICAS_LENGTH_TOTAL]

        for key, v in season[k.REPLICAS_LENGTH_LIST].iteritems():
            if key not in self._replicasLength_List:
                self._replicasLength_List[key] = v
            else:
                self._replicasLength_List[key] += v

    def calculate_configuration_matrix(self):

        header = ["Speaker/Season"] + ["Season " + str(i) for i in xrange(1, self._number_of_seasons + 1)]
        conf_matrix = []

        speakers = deepcopy(self._speakers)
        speakers.sort(key=lambda x: len(x[k.APPEARED_IN_SEASONS]), reverse=True)

        for speaker in speakers:
            _row = [speaker[k.NAME]]
            for i in xrange(1, self._number_of_seasons + +1):
                if i in speaker[k.APPEARED_IN_SEASONS]:
                    _row.append(1)
                else:
                    _row.append(0)
            conf_matrix.append(_row)

        self._configuration_matrix = conf_matrix

    def calculate_configuration_density(self):

        ones = 0

        for i in range(1, len(self._configuration_matrix)):
            row = self._configuration_matrix[i]

            ones += row[1:].count(1)

        self._configuration_density = float(ones) / (self._number_of_seasons * len(self._speakers))

    def calculate_force_related_graph_for_speakers(self, episodes):
        self._speakers = sorted(self._speakers, key=lambda key: key[k.NUMBER_OF_REPLICAS], reverse=True)

        episodes = list(episodes)

        force_directed_data = {
            'nodes': [],
            'links': []
        }
        count = 0

        links = []
        relations = {}

        speaker_count = 0
        speaker_index = {}

        for episode in episodes:

            epi_force_data = episode.get(k.FORCE_DIRECTED_DATA)

            for link in epi_force_data[k.LINKS]:
                if link[k.SOURCE] not in k.TOP_20_NAMES or link[k.TARGET] not in k.TOP_20_NAMES:
                    continue

                relation_tuple = (link[k.SOURCE], link[k.TARGET])

                if relation_tuple not in relations:
                    relations[relation_tuple] = {
                        link[k.TYPE]: 1,
                        'encounters': link[k.WEIGHT]
                    }
                else:
                    if link[k.TYPE] in relations[relation_tuple]:
                        relations[relation_tuple][link[k.TYPE]] += 1
                    else:
                        relations[relation_tuple][link[k.TYPE]] = 1
                    relations[relation_tuple]['encounters'] += link[k.WEIGHT]

        calc_links = []

        new_relations_dict = {}

        for speakers, relation in relations.iteritems():
            speakers_rev = (speakers[1], speakers[0])

            if speakers not in new_relations_dict and speakers_rev not in new_relations_dict:
                new_relations_dict[speakers] = relation

            if speakers not in new_relations_dict and speakers_rev in new_relations_dict:

                old_relation = new_relations_dict.get(speakers_rev)

                old_relation[k.INDEPENDENT] = old_relation.get(k.INDEPENDENT, 0) + relation.get(k.INDEPENDENT, 0)
                old_relation[k.CONCOMIDANT] = old_relation.get(k.CONCOMIDANT, 0) + relation.get(k.CONCOMIDANT, 0)
                old_relation[k.ALTERNATIVE] = old_relation.get(k.ALTERNATIVE, 0) + relation.get(k.ALTERNATIVE, 0)
                old_relation['encounters'] = old_relation['encounters'] + relation['encounters']

                old_rel_dom = old_relation.get(k.DOMINATING, 0)
                old_rel_sub = old_relation.get(k.SUBORDINATING, 0)
                new_rel_dom = relation.get(k.DOMINATING, 0)
                new_rel_sub = relation.get(k.SUBORDINATING, 0)

                if old_rel_dom:
                    old_relation[k.DOMINATING] += new_rel_sub
                if old_rel_sub:
                    old_relation[k.SUBORDINATING] += new_rel_dom

                new_relations_dict[speakers_rev] = old_relation
                print "xxx"

        for speakers, relation in new_relations_dict.iteritems():

            max_relation_name = max(relation.iteritems(), key=operator.itemgetter(1))[0]
            relation_name = max_relation_name if relation[max_relation_name] > 0 else k.ALTERNATIVE

            if relation_name == 'encounters':
                rels = sorted(((v, key) for key, v in relation.items()))
                relation_name = rels[-2][1] if rels[-2][1] != 'encounters' else rels[-1][1]

            if speakers[0] not in k.TOP_20_NAMES or speakers[1] not in k.TOP_20_NAMES or relation_name == k.ALTERNATIVE:
                continue

            for speaker in speakers:
                if speaker not in force_directed_data[k.NODES]:
                    force_directed_data['nodes'].append({
                        "name": speaker,
                        "group": 1
                    })

            weight = relation[relation_name]

            if relation_name == k.SUBORDINATING:
                relation_name = k.DOMINATING
                speakers = (speakers[1], speakers[0])

            calc_links.append({
                k.SOURCE: speakers[0],
                k.TARGET: speakers[1],
                k.WEIGHT: relation['encounters'],
                k.TYPE: relation_name
            })

        force_directed_data['links'] = calc_links

        self._force_directed_data = force_directed_data

    def calculate_hamming_strings_for_speakers(self):

        new_speaker_list = []
        for speaker in deepcopy(self._speakers):
            hamm_dist_string = ""

            for i in range(1, self._number_of_seasons + 1):
                hamm_dist_string += "1" if i in speaker[k.APPEARED_IN_SEASONS] else "0"

            speaker[k.HAMMING_STRING] = hamm_dist_string
            new_speaker_list.append(speaker)
        self._speakers = new_speaker_list
