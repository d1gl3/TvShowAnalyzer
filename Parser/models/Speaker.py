from Parser.models.BaseModel import BaseModel
from Parser.utils import *
import keywords as k


class Speaker(BaseModel):
    def __init__(self, name):
        BaseModel.__init__(self)
        self._name = name

    def add_replica(self, scene_number, episode_number, season_number, replik_length):
        if replik_length in self._replicasLength_List:
            self._replicasLength_List["_%s" % replik_length] += 1
        else:
            self._replicasLength_List["_%s" % replik_length] = 1
        self._number_of_replicas += 1
        self._replicasLength_total += replik_length

        if scene_number not in self._appeared_in_scenes:
            self._appeared_in_scenes.append(int(scene_number))
        if episode_number not in self._appeared_in_episodes:
            self._appeared_in_episodes.append(int(episode_number))
        if season_number not in self._appeared_in_seasons:
            self._appeared_in_seasons.append(int(season_number))

    def calculate_replica_statistics(self):
        if self._replicasLength_List:
            lengths = []
            for key, v in self._replicasLength_List.iteritems():
                key = key[1:]
                for i in range(v):
                    lengths.append(key)
            self._replicasLength_avg = mean(lengths)
            self._replicasLength_med = median(lengths)
            self._replicasLength_max = max(lengths)
            self._replicasLength_min = min(lengths)

    def get_json(self):
        return {
            k.APPEARED_IN_SCENES: self._appeared_in_scenes,
            k.APPEARED_IN_EPISODES: self._appeared_in_episodes,
            k.APPEARED_IN_SEASONS: self._appeared_in_episodes,
            "_id": self._id,
            k.NAME: self._name,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.REPLIK_PERCENTAGE: self._scene_replic_percentage,
            k.WORD_PERCENTAGE: self._scene_word_percentage
        }
