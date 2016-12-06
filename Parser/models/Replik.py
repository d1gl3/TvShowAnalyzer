import keywords as k


class Replik:
    def __init__(self):
        self._speaker = None
        self._replik = None
        self._replik_word_count = None
        self._scene_number = None
        self._episode_number = None
        self._season_number = None
        self._replik_number = None

    def get_json(self):
        return {
            k.SPEAKER: self._speaker,
            k.REPLIK: self._replik,
            k.WORD_COUNT: self._replik_word_count,
            k.SCENE_NUMBER: self._scene_number,
            k.EPISODE_NUMBER: self._episode_number,
            k.SEASON_NUMBER: self._season_number,
            "replik_number": self._replik_number
        }
