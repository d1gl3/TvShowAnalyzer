from BaseModel import BaseModel
from copy import deepcopy
from Parser.utils import *
import keywords as k


class TvShow(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)

    def get_json(self):
        return {
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
            k.CONFIGURATION_DENSITY: self._configuration_density
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
                old_replica_length_list.extend(speaker.get(k.REPLICAS_LENGTH_LIST, 0))
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_LIST] = old_replica_length_list
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_TOTAL] += speaker.get(k.REPLICAS_LENGTH_TOTAL, 0)
                old_appeared_in_seasons_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SEASONS]
                for season_number in speaker.get(k.APPEARED_IN_SEASONS, []):
                    if season_number not in old_appeared_in_seasons_list:
                        old_appeared_in_seasons_list.append(season_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SEASONS] = old_appeared_in_seasons_list

        speakers = [v for speaker, v in new_speakers_dict.iteritems()]

        for speaker in speakers:
            speaker[k.SEASON_WORD_PERCENTAGE] = float(speaker[k.REPLICAS_LENGTH_TOTAL]) / float(
                self._replicasLength_total)
            speaker[k.SEASON_REPLIK_PERCENTAGE] = float(speaker[k.NUMBER_OF_REPLICAS]) / float(self._number_of_replicas)
            speaker[k.REPLICAS_LENGTH_AVERAGE] = mean(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MEDIAN] = median(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MAX] = max(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MIN] = min(speaker[k.REPLICAS_LENGTH_LIST])
            new_speakers.append(speaker)
        self._speakers = new_speakers

    def add_season(self, season):
        self._number_of_seasons += 1
        self._number_of_replicas += season[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += season[k.REPLICAS_LENGTH_TOTAL]
        self._replicasLength_List.extend(season[k.REPLICAS_LENGTH_LIST])

    def calculate_configuration_matrix(self):

        header = ["Speaker/Season"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_seasons + 1):
            _row = [i]
            for speaker in self._speakers:
                _appeared_in = speaker[k.APPEARED_IN_SEASONS]
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

        self._configuration_density = float(ones) / (self._number_of_seasons * len(self._speakers))
