from Parser.utils import *
import keywords as k


# Base class to prevent redundancy
class BaseModel:
    def __init__(self):

        self._appeared_in_episodes = []
        self._appeared_in_scenes = []
        self._appeared_in_seasons = []
        self._configuration_density = None
        self._configuration_matrix = None
        self._episode_number = None
        self._id = None
        self._name = None
        self._number_of_episodes = 0
        self._number_of_replicas = 0
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
