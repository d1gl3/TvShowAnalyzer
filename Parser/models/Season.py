from copy import deepcopy

import itertools

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
            k.SPEAKERS: self._speakers
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

        header = ["Speaker/Episode"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_episodes + 1):
            _row = ["Episode " + str(i)]
            for speaker in self._speakers:
                _appeared_in = speaker[k.APPEARED_IN_EPISODES]
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

        for episode in episodes:
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

            source = int(speaker_index[link[0]])
            target = int(speaker_index[link[1]])
            value = int(link[2])

            if source is not None and target is not None and value is not None:

                calc_links.append({
                    'source': source,
                    'target': target,
                    'weight': value
                })
            else:
                print "x"

        force_directed_data['links'] = calc_links

        self._force_directed_data = force_directed_data

    def calculate_burst_chart_for_number_of_replicas(self, scenes):
        burst_dict_season = {
            "name": "Season_%s" % self._season_number,
            "children": []
        }

        help_dict = {}

        for scene in scenes:
            _scene_episode = scene[k.EPISODE_NUMBER]
            _scene_number = scene[k.SCENE_NUMBER]
            _scene_number_of_replicas = scene[k.NUMBER_OF_REPLICAS]

            if _scene_episode not in help_dict:
                help_dict[_scene_episode] = {}

            help_dict[_scene_episode][_scene_number] = _scene_number_of_replicas

        season_children = []

        for episode_number, episode in help_dict.iteritems():
            burst_dict_episode = {
                "name": "Episode_%s" % episode_number
            }

            episode_children = []
            for scene_number, value in episode.iteritems():
                burst_dict_scene = {
                    "name": "Scene_%s" % scene_number,
                    "size": value
                }

                episode_children.append(burst_dict_scene)

            burst_dict_episode['children'] = episode_children
            season_children.append(burst_dict_episode)

        burst_dict_season['children'] = season_children

        print burst_dict_season

    def calculate_hamming_strings_for_speakers(self):

        new_speaker_list = []
        for speaker in deepcopy(self._speakers):
            hamm_dist_string = ""

            for i in range(1, self._number_of_episodes + 1):
                hamm_dist_string += "1" if i in speaker[k.APPEARED_IN_EPISODES] else "0"

            speaker[k.HAMMING_STRING] = hamm_dist_string
            new_speaker_list.append(speaker)
        self._speakers = new_speaker_list
