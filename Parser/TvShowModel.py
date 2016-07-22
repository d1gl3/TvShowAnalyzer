from copy import deepcopy

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
        self._speakers = []
        self._title = None


class Season:

    def __init__(self):

        self._replicasLength_total = None
        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_episodes = None
        self._number_of_replicas = None
        self._number_of_speakers = None
        self._replicasLength_avg = None
        self._replicasLength_max = None
        self._replicasLength_med = None
        self._replicasLength_min = None
        self._season_number = None
        self._speakers = []

    def get_json(self):
        return {
            k.CONFIGURATION_DENSITY: self._configuration_density,
            k.CONFIGURATION_MATRIX: self._configuration_matrix,
            k.NUMBER_OF_EPISODES: self._number_of_episodes,
            k.NUMBER_OF_REPLICAS: self._number_of_replicas,
            k.NUMBER_OF_SPEAKERS: self._number_of_speakers,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.SEASON_NUMBER: self._season_number,
            k.SPEAKERS: self._speakers
        }


class Episode:

    def __init__(self):

        self._configuration_density = None
        self._configuration_matrix = None
        self._episode_number = None
        self._number_of_replicas = 0
        self._number_of_scenes = 0
        self._replicasLength_avg = 0
        self._replicasLength_List = []
        self._replicasLength_max = 0
        self._replicasLength_med = 0
        self._replicasLength_min = 0
        self._replicasLength_total = 0
        self._season_number = None
        self._speakers = []

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

    def add_speaker(self, speaker):
        self._speakers.append(speaker)

    def add_scene(self, scene):
        self._number_of_scenes += 1
        self._number_of_replicas += scene[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += scene[k.REPLICAS_LENGTH_TOTAL]
        self._replicasLength_List.extend(scene[k.REPLICAS_LENGTH_LIST])

    def calculate_replica_statistics(self):
        self._replicasLength_avg = mean(self._replicasLength_List)
        self._replicasLength_med = median(self._replicasLength_List)
        self._replicasLength_max = max(self._replicasLength_List)
        self._replicasLength_min = min(self._replicasLength_List)

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


class Scene:

    def __init__(self):

        self._episode_number = None
        self._number_of_replicas = 0
        self._number_of_speakers = 0
        self._replicasLength_total = 0
        self._replicasLength_avg = 0
        self._replicasLength_max = 0
        self._replicasLength_med = 0
        self._replicasLength_min = 0
        self._replicasLength_List = []

        self._scene_number = None
        self._season_number = None
        self._speakers = []

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

    def add_speaker(self, speaker):
        self._speakers.append(speaker)

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
            k.SCENE_NUMBER: self._scene_number,
            k.EPISODE_NUMBER: self._episode_number,
            k.SEASON_NUMBER: self._season_number
        }


class Speaker:
    def __init__(self, name):
        self._name = name
        self._number_of_replics = 0
        self._replicasLength_avg = 0
        self._replicasLength_List = []
        self._replicasLength_max = 0
        self._replicasLength_med = 0
        self._replicasLength_min = 0
        self._replicasLength_total = 0
        self._scene_replic_percentage = 0
        self._scene_word_percentage = 0

    def add_replica(self, replik_length):
        self._replicasLength_List.append(replik_length)
        self._number_of_replics += 1
        self._replicasLength_total += replik_length

    def calculate_replica_statistics(self):
        if self._replicasLength_List:
            self._replicasLength_avg = mean(self._replicasLength_List)
            self._replicasLength_med = median(self._replicasLength_List)
            self._replicasLength_max = max(self._replicasLength_List)
            self._replicasLength_min = min(self._replicasLength_List)

    def get_json(self):
        return {
            k.NAME: self._name,
            k.NUMBER_OF_REPLICAS: self._number_of_replics,
            k.REPLICAS_LENGTH_AVERAGE: self._replicasLength_avg,
            k.REPLICAS_LENGTH_TOTAL: self._replicasLength_total,
            k.REPLICAS_LENGTH_MAX: self._replicasLength_max,
            k.REPLICAS_LENGTH_MIN: self._replicasLength_min,
            k.REPLICAS_LENGTH_MEDIAN: self._replicasLength_med,
            k.REPLICAS_LENGTH_LIST: self._replicasLength_List,
            k.SCENE_REPLIK_PERCENTAGE: self._scene_replic_percentage,
            k.SCENE_WORD_PERCENTAGE: self._scene_word_percentage
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
