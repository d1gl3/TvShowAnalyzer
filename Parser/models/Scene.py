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
        self._replicasLength_List.append(replik_length)
        self._number_of_replicas += 1
        self._replicasLength_total += replik_length

    def calculate_replica_statistics(self):
        if not self._replicasLength_List:
            print self._season_number, self._episode_number, self._scene_number
        else:
            self._replicasLength_avg = mean(self._replicasLength_List)
            self._replicasLength_med = median(self._replicasLength_List)
            self._replicasLength_max = max(self._replicasLength_List)
            self._replicasLength_min = min(self._replicasLength_List)

    def calculate_speaker_statistics(self):
        speakers = deepcopy(self._speakers)
        new_speakers = []
        for speaker in speakers:
            speaker[k.SCENE_WORD_PERCENTAGE] = float(speaker[k.REPLICAS_LENGTH_TOTAL]) / float(self._replicasLength_total)
            speaker[k.SCENE_REPLIK_PERCENTAGE] = float(speaker[k.NUMBER_OF_REPLICAS]) / float(self._number_of_replicas)
            if speaker[k.REPLICAS_LENGTH_LIST]:
                speaker[k.REPLICAS_LENGTH_AVERAGE] = mean(speaker[k.REPLICAS_LENGTH_LIST])
                speaker[k.REPLICAS_LENGTH_MEDIAN] = median(speaker[k.REPLICAS_LENGTH_LIST])
                speaker[k.REPLICAS_LENGTH_MAX] = max(speaker[k.REPLICAS_LENGTH_LIST])
                speaker[k.REPLICAS_LENGTH_MIN] = min(speaker[k.REPLICAS_LENGTH_LIST])
            new_speakers.append(speaker)
        self._speakers = new_speakers
