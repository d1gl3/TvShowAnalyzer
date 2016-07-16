from utils import *
import keywords as k

class TvShow:

    def __init__(self):

        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_replicas = None
        self._number_of_seasons = None
        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_med = None
        self._replicasLength_min = None
        self._seasons = None
        self._speakers = None
        self._title = None


class Season:

    def __init__(self):

        self._acts = None
        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_acts = None
        self._number_of_replicas = None
        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_med = None
        self._replicasLength_min = None
        self._season_number = None
        self._speakers = None


class Act:

    def __init__(self):

        self._act_number = None
        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_replicas = None
        self._number_of_scenes = None
        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_med = None
        self._replicasLength_min = None
        self._scenes = None
        self._season_number = None
        self._speakers = None


class Scene:

    def __init__(self):

        self._act_number = None
        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_replicas = None
        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_med = None
        self._replicasLength_min = None
        self._scene_number = None
        self._season_number = None
        self._speakers = None


class Replik:
    def __init__(self):
        self._speaker = None
        self._replik = None
        self._replik_word_count = None
        self._scene_number = None
        self._episode_number = None
        self._season_number = None

    def get_json(self):
        return {
            k.SPEAKER: self._speaker,
            k.REPLIK: self._replik,
            k.WORD_COUNT: self._replik_word_count,
            k.SCENE: self._scene_number,
            k.EPISODE: self._episode_number,
            k.SEASON: self._season_number
        }


class ConfigurationModel:
    def __init__(self):

        self._number = None
        self._replicas = None
        self._appearing_speakers = None

        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_min = None
        self._replicasLength_med = None

    def calc_replicas_statistics(self):
        replicas = self._replicas
        replicas_lengths = []
        for replica in replicas:
            replicas_lengths.append(replica.word_count)

        if replicas:
            self._replicasLength_avg = mean(replicas_lengths)
            self._replicasLength_max = max(replicas_lengths)
            self._replicasLength_min = min(replicas_lengths)
            self._replicasLength_med = median(replicas_lengths)
