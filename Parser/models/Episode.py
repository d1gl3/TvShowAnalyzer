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
            k.SPEAKERS: self._speakers
        }

    def add_scene(self, scene):
        self._number_of_scenes += 1
        self._number_of_replicas += scene[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += scene[k.REPLICAS_LENGTH_TOTAL]
        for key, v in scene[k.REPLICAS_LENGTH_LIST].iteritems():
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

        header = ["Speaker/Scene"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_scenes + 1):
            _row = ["Scene " + str(i)]
            for speaker in self._speakers:
                _appeared_in = speaker[k.APPEARED_IN_SCENES]
                if i in _appeared_in:
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
                "group": (1 if count < 20 else 2)
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
            calc_links.append({
                'source': int(speaker_index[link[0]]),
                'target': int(speaker_index[link[1]]),
                'weight': int(link[2])
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
