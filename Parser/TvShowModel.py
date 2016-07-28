from copy import deepcopy

from utils import *
import keywords as k


# Base class to prevent redundancy
class BaseClass:
    def __init__(self):

        self._appeared_in_episodes = []
        self._appeared_in_scenes = []
        self._configuration_density = None
        self._configuration_matrix = None
        self._episode_number = None
        self._number_of_episodes = 0
        self._number_of_replics = 0
        self._number_of_scenes = 0
        self._number_of_seasons = 0
        self._number_of_speakers = 0
        self._replicasLength_avg = 0
        self._replicasLength_List = []
        self._replicasLength_max = 0
        self._replicasLength_med = 0
        self._replicasLength_min = 0
        self._replicasLength_total = 0
        self._scene_number = None
        self._scene_replic_percentage = 0
        self._scene_word_percentage = 0
        self._season_number = None
        self._speakers = []
        self._title = None

    def add_speaker(self, speaker):
        self._speakers.append(speaker)

    def calculate_replica_statistics(self):
        self._replicasLength_avg = mean(self._replicasLength_List)
        self._replicasLength_med = median(self._replicasLength_List)
        self._replicasLength_max = max(self._replicasLength_List)
        self._replicasLength_min = min(self._replicasLength_List)

    def calculate_speaker_relations(self):
        updated_speakers = []
        for speaker_a in self._speakers:
            speaker_a[k.CONCOMIDANT] = []
            speaker_a[k.DOMINATING] = []
            speaker_a[k.SUBORDINATING] = []
            speaker_a[k.INDEPENDENT] = []
            speaker_a[k.ALTERNATIVE] = []

            _appears_in_a = speaker_a[k.APPEARED_IN_SCENES]

            for speaker_b in self._speakers:
                # Skip calculating relation with same speaker
                if speaker_a[k.NAME] == speaker_b[k.NAME]:
                    continue

                _appears_in_b = speaker_b[k.APPEARED_IN_SCENES]

                if set(_appears_in_a) == set(_appears_in_b):
                    if speaker_b[k.NAME] not in speaker_a[k.CONCOMIDANT]:
                        speaker_a[k.CONCOMIDANT].append(speaker_b[k.NAME])
                elif set(_appears_in_b) < set(_appears_in_a):
                    speaker_a[k.DOMINATING].append(speaker_b[k.NAME])
                elif set(_appears_in_a) < set(_appears_in_b):
                    speaker_a[k.SUBORDINATING].append(speaker_b[k.NAME])
                else:
                    speaker_a[k.INDEPENDENT].append(speaker_b[k.NAME])

                if not any(i in _appears_in_a for i in _appears_in_b):
                    speaker_a[k.ALTERNATIVE].append(speaker_b[k.NAME])

            updated_speakers.append(speaker_a)
        self._speakers = updated_speakers


class TvShow(BaseClass):

    def __init__(self):

        BaseClass.__init__(self)


    def get_json(self):
        return {
            k.NUMBER_OF_EPISODES: self._number_of_episodes,
            k.NUMBER_OF_REPLICAS: self._number_of_replics,
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
            speaker[k.SEASON_REPLIK_PERCENTAGE] = float(speaker[k.NUMBER_OF_REPLICAS]) / float(self._number_of_replics)
            speaker[k.REPLICAS_LENGTH_AVERAGE] = mean(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MEDIAN] = median(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MAX] = max(speaker[k.REPLICAS_LENGTH_LIST])
            speaker[k.REPLICAS_LENGTH_MIN] = min(speaker[k.REPLICAS_LENGTH_LIST])
            new_speakers.append(speaker)
        self._speakers = new_speakers

    def add_season(self, season):
        self._number_of_seasons += 1
        self._number_of_replics += season[k.NUMBER_OF_REPLICAS]
        self._replicasLength_total += season[k.REPLICAS_LENGTH_TOTAL]
        self._replicasLength_List.extend(season[k.REPLICAS_LENGTH_LIST])


    def calculate_configuration_matrix(self):

        header = ["Speaker/Season"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_seasons + 1):
            _row = []
            _row.append(i)
            for speaker in self._speakers:
                _name = speaker[k.NAME]
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

class Season(BaseClass):

    def __init__(self):
        BaseClass.__init__(self)
        self._replicasLength_total = None
        self._configuration_density = None
        self._configuration_matrix = None
        self._number_of_episodes = 0
        self._number_of_replicas = 0
        self._number_of_speakers = 0
        self._replicasLength_avg = 0
        self._replicasLength_max = 0
        self._replicasLength_med = 0
        self._replicasLength_min = 0
        self._replicasLength_List = []
        self._replicasLength_total = 0
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
                old_replica_length_list.extend(speaker.get(k.REPLICAS_LENGTH_LIST, 0))
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_LIST] = old_replica_length_list
                new_speakers_dict[speaker[k.NAME]][k.REPLICAS_LENGTH_TOTAL] += speaker.get(k.REPLICAS_LENGTH_TOTAL, 0)
                old_appeared_in_episode_list = new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_EPISODES]
                for episode_number in speaker.get(k.APPEARED_IN_EPISODES, []):
                    if episode_number not in old_appeared_in_episode_list:
                        old_appeared_in_episode_list.append(episode_number)
                new_speakers_dict[speaker[k.NAME]][k.APPEARED_IN_SCENES] = old_appeared_in_episode_list

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

        header = ["Speaker/Episode"] + [speaker[k.NAME] for speaker in self._speakers]
        conf_matrix = [header]

        for i in range(1, self._number_of_episodes + 1):
            _row = [i]
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
        self._replicasLength_List.extend(episode[k.REPLICAS_LENGTH_LIST])


class Episode(BaseClass):

    def __init__(self):

        BaseClass.__init__(self)
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
            _row = []
            _row.append(i)
            for speaker in self._speakers:
                _name = speaker[k.NAME]
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


class Scene(BaseClass):

    def __init__(self):

        BaseClass.__init__(self)
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
        self._id = None
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
        self._appeared_in_scenes = []
        self._appeared_in_episodes = []
        self._appeared_in_seasons = []

    def add_replica(self, scene_number, episode_number, season_number, replik_length):
        self._replicasLength_List.append(replik_length)
        self._number_of_replics += 1
        self._replicasLength_total += replik_length

        if scene_number not in self._appeared_in_scenes:
            self._appeared_in_scenes.append(scene_number)
        if episode_number not in self._appeared_in_episodes:
            self._appeared_in_episodes.append(episode_number)
        if season_number not in self._appeared_in_seasons:
            self._appeared_in_seasons.append(season_number)

    def calculate_replica_statistics(self):
        if self._replicasLength_List:
            self._replicasLength_avg = mean(self._replicasLength_List)
            self._replicasLength_med = median(self._replicasLength_List)
            self._replicasLength_max = max(self._replicasLength_List)
            self._replicasLength_min = min(self._replicasLength_List)

    def get_json(self):
        return {
            k.APPEARED_IN_SCENES: self._appeared_in_scenes,
            k.APPEARED_IN_EPISODES: self._appeared_in_episodes,
            k.APPEARED_IN_SEASONS: self._appeared_in_episodes,
            "_id": self._id,
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