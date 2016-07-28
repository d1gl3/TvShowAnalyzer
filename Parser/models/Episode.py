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
        self._replicasLength_List.extend(scene[k.REPLICAS_LENGTH_LIST])

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
                old_replica_length_list.extend(speaker.get(k.REPLICAS_LENGTH_LIST, 0))
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_LIST] = old_replica_length_list
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_TOTAL] += speaker.get(k.REPLICAS_LENGTH_TOTAL, 0)
                old_appeared_in_scene_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SCENES]
                for scene_number in speaker.get(k.APPEARED_IN_SCENES, []):
                    if scene_number not in old_appeared_in_scene_list:
                        old_appeared_in_scene_list.append(scene_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SCENES] = old_appeared_in_scene_list

        speakers = [v for speaker, v in new_speakers_dict.iteritems()]

        for speaker in speakers:
            speaker[k.EPISODE_WORD_PERCENTAGE] = float(speaker[k.REPLICAS_LENGTH_TOTAL]) / float(
                self._replicasLength_total)
            speaker[k.EPISODE_REPLIK_PERCENTAGE] = float(speaker[k.NUMBER_OF_REPLICAS]) / float(self._number_of_replicas)
            speaker[k.REPLICAS_LENGTH_AVERAGE] = mean(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MEDIAN] = median(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MAX] = max(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MIN] = min(speaker[k.REPLICAS_LENGTH_LIST])
            new_speakers.append(speaker)
        self._speakers = new_speakers

    def calculate_configuration_matrix(self):

        header = ["Speaker/Scene"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_scenes + 1):
            _row = [i]
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
