from copy import deepcopy

import itertools

import operator

from Parser.models.BaseModel import BaseModel
from Parser.utils import *
import keywords as k


class Season(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)

    def get_json(self):
        return {
            k.CONFIGURATION_DENSITY: self._configuration_density,
            k.CONFIGURATION_MATRIX: self._configuration_matrix,
            k.FORCE_DIRECTED_DATA: self._force_directed_data,
            k.NUMBER_OF_EPISODES: self._number_of_episodes,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.NUMBER_OF_SPEAKERS: self._number_of_speakers,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.SEASON_NUMBER: self._season_number,
            k.SPEAKERS: self._speakers,
            k.PROBABILITY_MATRIX: self._probability_matrix
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
                old_appeared_in_episode_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_EPISODES]
                for episode_number in speaker.get(k.APPEARED_IN_EPISODES, []):
                    if episode_number not in old_appeared_in_episode_list:
                        old_appeared_in_episode_list.append(episode_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_EPISODES] = old_appeared_in_episode_list

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

    def calculate_configuration_matrix(self):

        header = ["Speaker/Episode"] + ["Episode " + str(i) for i in xrange(1, self._number_of_episodes + 1)]
        conf_matrix = [header]

        speakers = deepcopy(self._speakers)
        speakers.sort(key=lambda x: len(x[k.APPEARED_IN_EPISODES]), reverse=True)

        for speaker in speakers:
            _row = [speaker[k.NAME]]
            for i in xrange(1, self._number_of_episodes + +1):
                if i in speaker[k.APPEARED_IN_EPISODES]:
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

        self._configuration_density = float(ones) / (self._number_of_episodes * len(self._speakers))

    def add_episode(self, episode):
        self._number_of_episodes += 1
        self._number_of_replicas += episode[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += episode[k.REPLICAS_LENGTH_TOTAL]

        for key, v in episode[k.REPLICAS_LENGTH_LIST].iteritems():
            if key not in self._replicasLength_List:
                self._replicasLength_List[key] = v
            else:
                self._replicasLength_List[key] += v

    @property
    def season_number(self):
        return self._season_number

    def calculate_force_related_graph_for_speakers(self, episodes):
        self._speakers = sorted(self._speakers, key=lambda key: key[k.NUMBER_OF_REPLICAS], reverse=True)

        force_directed_data = {
            'nodes': [],
            'links': []
        }
        count = 0

        links = []

        speaker_count = 0
        speaker_index = {}

        relations = {}

        for episode in episodes:
            epi_force_data = episode.get(k.FORCE_DIRECTED_DATA)

            for link in epi_force_data[k.LINKS]:

                relation_tuple = (link[k.SOURCE], link[k.TARGET])

                if relation_tuple not in relations:
                    relations[relation_tuple] = {
                        link[k.TYPE]: 1
                    }
                else:
                    if link[k.TYPE] in relations[relation_tuple]:
                        relations[relation_tuple][link[k.TYPE]] += 1
                    else:
                        relations[relation_tuple][link[k.TYPE]] = 1

            """
            speakers = deepcopy(episode[k.SPEAKERS])

            for s_a in speakers:
                s_a_scenes = s_a[k.APPEARED_IN_SCENES]

                if s_a[k.NAME] not in k.TOP_20_NAMES:
                    continue

                if s_a[k.NAME] not in speaker_index:
                    force_directed_data['nodes'].append({
                        "name": s_a[k.NAME],
                        "group": (1 if count < 5 else 2)
                    })
                    count += 1

                    speaker_index[s_a[k.NAME]] = speaker_count
                    speaker_count += 1

                for s_b in speakers:
                    if s_a[k.NAME] == s_b[k.NAME]:
                        continue

                    if s_b[k.NAME] not in k.TOP_20_NAMES:
                        continue

                    if (s_b[k.NAME], s_a[k.NAME]) in links:
                        continue

                    s_b_scenes = s_b[k.APPEARED_IN_SCENES]

                    common_scenes = list(set(s_a_scenes).intersection(s_b_scenes))

                    for season in common_scenes:
                        links.append(
                            (s_a[k.NAME], s_b[k.NAME])
                        )

        dict_a = {row: 0 for row in links}
        for row in links:
            if row in dict_a:
                dict_a[row] += 1

        result = set([row + (dict_a[row],) for row in links])

        nodes = {}
        calc_links = []
        for link in result:

            for speaker in self._speakers:
                if speaker[k.NAME] == link[0]:
                    if link[1] in speaker[k.DOMINATING]:
                        type = k.DOMINATING
                    elif link[1] in speaker[k.SUBORDINATING]:
                        type = k.SUBORDINATING
                    elif link[1] in speaker[k.CONCOMIDANT]:
                        type = k.CONCOMIDANT
                    elif link[1] in speaker[k.ALTERNATIVE]:
                        type = k.ALTERNATIVE
                    elif link[1] in speaker[k.INDEPENDENT]:
                        type = k.INDEPENDENT

            calc_links.append({
                'source': link[0],
                'target': link[1],
                'weight': int(link[2]),
                'type': type
            })
        """

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

            sum_episodes_together = sum(relation.values())
            max_relation_name = max(relation.iteritems(), key=operator.itemgetter(1))[0]
            relation_name = max_relation_name if relation[max_relation_name] > 0 else k.ALTERNATIVE



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
                k.WEIGHT: weight,
                k.TYPE: relation_name
            })

        force_directed_data['links'] = calc_links

        self._force_directed_data = force_directed_data

    def calculate_hamming_strings_for_speakers(self):

        new_speaker_list = []
        for speaker in deepcopy(self._speakers):
            hamm_dist_string = ""

            for i in range(1, self._number_of_episodes + 1):
                hamm_dist_string += "1" if i in speaker[k.APPEARED_IN_EPISODES] else "0"

            speaker[k.HAMMING_STRING] = hamm_dist_string
            new_speaker_list.append(speaker)
        self._speakers = new_speaker_list

    def calculate_speaker_probabilities(self, episodes):
        new_speaker_list = []

        speaker_scenes = {
            "single": {},
            "couple": {}
        }
        number_of_scenes_total = 0

        for epi in episodes:
            number_of_scenes_total += epi[k.NUMBER_OF_SCENES]

            for speaker in epi[k.SPEAKERS]:
                if speaker[k.NAME] not in speaker_scenes['single']:
                    speaker_scenes['single'][speaker[k.NAME]] = len(speaker[k.APPEARED_IN_SCENES])
                else:
                    speaker_scenes['single'][speaker[k.NAME]] += len(speaker[k.APPEARED_IN_SCENES])

            for speaker in epi[k.SPEAKERS]:
                for speaker_b in epi[k.SPEAKERS]:
                    if speaker[k.NAME] != speaker_b[k.NAME]:

                        key = tuple(sorted([speaker[k.NAME], speaker_b[k.NAME]]))

                        if key not in speaker_scenes['couple']:
                            speaker_scenes['couple'][key] = len(
                                list(set(speaker[k.APPEARED_IN_SCENES]) & set(speaker_b[k.APPEARED_IN_SCENES])))

        for speaker in deepcopy(speaker_scenes['single']):
            speaker_scenes['single'][speaker] /= float(number_of_scenes_total)

        speakers = deepcopy(self._speakers)
        sorted_speakers = sorted(speakers, key=lambda x: x[k.NAME])

        probability_matrix = [["Speakers"] + [s[k.NAME] for s in sorted_speakers]]

        for speaker_a in sorted_speakers:
            a_name = speaker_a[k.NAME]
            new_row = [a_name]
            for speaker_b in sorted_speakers:
                b_name = speaker_b[k.NAME]

                if a_name != b_name:
                    key = tuple(sorted([a_name, b_name]))

                    n_ij = speaker_scenes['couple'].get(key)

                    if not n_ij:
                        new_row.append("x")
                        continue

                    _n_ij = number_of_scenes_total * speaker_scenes['single'][key[0]] * speaker_scenes['single'][key[1]]

                    delta = n_ij - _n_ij

                    new_row.append(float("{:4.2f}".format(delta)))

                else:
                    new_row.append("-")

            probability_matrix.append(new_row)

        self._probability_matrix = probability_matrix


