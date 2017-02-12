import itertools
from pprint import pprint

from BaseModel import BaseModel
from copy import deepcopy
from Parser.utils import *
import keywords as k


class Episode(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)

    def get_json(self):
        return {
            k.EPISODE_NUMBER: self._episode_number,
            k.FORCE_DIRECTED_DATA: self._force_directed_data,
            k.CONFIGURATION_DENSITY: self._configuration_density,
            k.CONFIGURATION_MATRIX: self._configuration_matrix,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.NUMBER_OF_SCENES: self._number_of_scenes,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.SEASON_NUMBER: self._season_number,
            k.SPEAKERS: self._speakers,
            k.PROBABILITY_MATRIX: self._probability_matrix,
            k.SPEAKER_PROBABILITIES: self._speaker_probabilities
        }

    def add_scene(self, scene):
        self._number_of_scenes += 1
        self._number_of_replicas += scene.get(k.NUMBER_OF_REPLICAS, 0)
        self._replicasLength_total += scene.get(k.REPLICAS_LENGTH_TOTAL, 0)
        for key, v in scene.get(k.REPLICAS_LENGTH_LIST, {}).iteritems():
            if key not in self._replicasLength_List:
                self._replicasLength_List[key] = v
            else:
                self._replicasLength_List[key] += v

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

                old_appeared_in_scene_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SCENES]
                for scene_number in speaker.get(k.APPEARED_IN_SCENES, []):
                    if scene_number not in old_appeared_in_scene_list:
                        old_appeared_in_scene_list.append(scene_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SCENES] = old_appeared_in_scene_list

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

        header = ["Speaker/Scene"] + ["Scene " + str(i) for i in xrange(1, self._number_of_scenes + 1)]
        conf_matrix = []

        speakers = deepcopy(self._speakers)
        speakers.sort(key=lambda x: len(x[k.APPEARED_IN_SCENES]), reverse=True)

        for speaker in speakers:
            _row = [speaker[k.NAME]]
            for i in xrange(1, self._number_of_scenes + +1):
                if i in speaker[k.APPEARED_IN_SCENES]:
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

        self._configuration_density = float(ones) / (self._number_of_scenes * len(self._speakers))

    def calculate_force_related_graph_for_speakers(self):
        self._speakers = sorted(self._speakers, key=lambda key: key[k.NUMBER_OF_REPLICAS], reverse=True)

        force_directed_data = {
            'nodes': [],
            'links': []
        }
        count = 0

        links = []

        all_combinations = list(itertools.combinations([speaker[k.NAME] for speaker in self._speakers], 2))

        speaker_count = 0
        speaker_index = {}

        for s_a in self._speakers:
            s_a_scenes = s_a[k.APPEARED_IN_SCENES]
            speaker_index[s_a[k.NAME]] = speaker_count
            speaker_count += 1
            node = {
                "name": s_a[k.NAME],
                "group": (1 if count < 5 else 2)
            }
            force_directed_data['nodes'].append(node)
            for s_b in self._speakers:
                if s_a[k.NAME] == s_b[k.NAME]:
                    continue

                if (s_b[k.NAME], s_a[k.NAME]) in links:
                    continue

                s_b_scenes = s_b[k.APPEARED_IN_SCENES]

                common_seasons = list(set(s_a_scenes).intersection(s_b_scenes))

                for season in common_seasons:
                    links.append(
                        (s_a[k.NAME], s_b[k.NAME])
                    )

            count += 1

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

        force_directed_data['links'] = calc_links

        self._force_directed_data = force_directed_data

    def calculate_hamming_strings_for_speakers(self):

        new_speaker_list = []
        for speaker in deepcopy(self._speakers):
            hamm_dist_string = ""

            for i in range(1, self._number_of_scenes + 1):
                hamm_dist_string += "1" if i in speaker[k.APPEARED_IN_SCENES] else "0"

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

        couple_count = {}
        for key, v in speaker_scenes['couple'].iteritems():
            if key[0].replace(".", "") not in couple_count:
                couple_count[key[0].replace(".", "")] = {}
            if key[1].replace(".", "") not in couple_count:
                couple_count[key[1].replace(".", "")] = {}

            couple_count[key[0].replace(".", "")][key[1].replace(".", "")] = v
            couple_count[key[1].replace(".", "")][key[0].replace(".", "")] = v
        speaker_scenes['couple'] = couple_count

        for key, v in speaker_scenes['single'].iteritems():
            if "." in key:
                speaker_scenes['single'][key.replace(".", "")] = v
                del speaker_scenes['single'][key]


        self._speaker_probabilities = speaker_scenes
        self._probability_matrix = probability_matrix


