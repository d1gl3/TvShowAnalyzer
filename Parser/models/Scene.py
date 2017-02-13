from BaseModel import BaseModel
from copy import deepcopy
from Parser.utils import *
import keywords as k


class Scene(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)

    def get_json(self):
        return {
            k.EPISODE_NUMBER: self._episode_number,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.NUMBER_OF_SPEAKERS: self._number_of_speakers,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.SCENE_NUMBER: self._scene_number,
            k.SEASON_NUMBER: self._season_number,
            k.SPEAKERS: self._speakers
        }

    def add_replica(self, replik_length):
        if "_%s" % replik_length in self._replicasLength_List:
            self._replicasLength_List["_%s" % replik_length] += 1
        else:
            self._replicasLength_List["_%s" % replik_length] = 1
        self._number_of_replicas += 1
        self._replicasLength_total += replik_length

    def calculate_replica_statistics(self):
        if not self._replicasLength_List:
            print self._season_number, self._episode_number, self._scene_number
        else:
            lengths = []
            for key, v in self._replicasLength_List.iteritems():
                key = key[1:]
                for i in range(v):
                    lengths.append(int(key))
            self._replicasLength_avg = mean(lengths)
            self._replicasLength_med = median(lengths)
            self._replicasLength_max = max(lengths)
            self._replicasLength_min = min(lengths)

    def calculate_speaker_statistics(self):
        speakers = deepcopy(self._speakers)
        new_speakers = []
        if self._replicasLength_total > 0 and self._number_of_replicas > 0:
            for speaker in speakers:
                speaker[k.WORD_PERCENTAGE] = float(speaker[k.REPLICAS_LENGTH_TOTAL]) / float(self._replicasLength_total)
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

