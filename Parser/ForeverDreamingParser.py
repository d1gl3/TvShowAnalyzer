import re
from HTMLParser import HTMLParser
import keywords as k
from MongoDB.MongoDBConnection import MongoDBConnection
from Parser.models.Replik import Replik
from Parser.models.Scene import Scene


class MyHTMLParser(HTMLParser):
    def __init__(self, season, episode):
        HTMLParser.__init__(self)

        self.mongo_db = MongoDBConnection()

        self.con = self.mongo_db.get_con()
        self.db = self.mongo_db.get_db_by_name(k.BIG_BANG_THEORY)
        self.episode = episode
        self.out = {"0": []}
        self.replik_coll = self.mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.REPLIK_COLLECTION)
        self.scene_coll = self.mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SCENE_COLLECTION)
        self.speaker_coll = self.mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.SPEAKER_COLLECTION)
        self.scene_count = 0
        self.season = season

    def handle_data(self, data):

        re_spoken = re.compile(r'[A-Z][a-z]+\s?(\([\sA-Za-z0-9]*\))?:')  # Regex to find repliks
        re_alpha_numeric = re.compile('[^a-zA-Z\s]')  # Regex to remove non alpha numeric characters
        re_quotation_marks = re.compile(
            ur'[\u0022\u0027\u00AB\u00BB\u2018\u2019\u201A\u201B\u201C\u201D\u201E\u201F\u2039'
            ur'\u203A\u300C\u300D\u300E\u300F\u301D\u301E\u301F\uFE41\uFE42\uFE43\uFE44\uFF02\uFF07\uFF62\uFF63]+')

        # Regex to remove any king of quotation marks

        # If html line starts with Scene, a new Scene is initialized and stored in MongoDB
        if data.startswith("Scene:") or data.startswith("</hr>"):
            if "%s" % self.scene_count not in self.out:
                self.out["%s" % self.scene_count] = []
            self.scene_count += 1
            if "%s" % self.scene_count not in self.out:
                self.out["%s" % self.scene_count] = []

            new_scene = Scene()
            new_scene._scene_number = self.scene_count
            new_scene._episode_number = self.episode
            new_scene._season_number = self.season

            self.scene_coll.insert(new_scene.get_json())

            return

        # Analyze Repliks
        if re.search(re_spoken, data) is not None:

            # Try to split Speaker name from Replik value
            try:
                speaker, replik = data.split(':', 1)
            except Exception, e:
                print e
                return

            # Strip all unwanted characters from Speaker and Replik Value
            speaker = re.sub("\(.*", "", speaker.decode('utf-8'))
            speaker = speaker.strip()
            replik = replik.decode('utf-8')
            replik = re.sub(re_quotation_marks, "", replik)
            replik = re.sub(re_alpha_numeric, "", replik)

            replik_word_count = len(replik.split())

            # Initiate new Replik object and insert in MongoDB
            new_replik = Replik()
            new_replik._speaker = speaker
            new_replik._replik = replik
            new_replik._replik_word_count = replik_word_count
            new_replik._scene_number = self.scene_count
            new_replik._episode_number = self.episode
            new_replik._season_number = self.season

            # self.out["%s" % self.scene_count][k.REPLIKS].append(new_replik)
            self.replik_coll.insert(new_replik.get_json())
            """
            try:
                speaker_obj = Speaker(speaker)
                speaker_obj._id = speaker
                self.speaker_coll.insert(speaker_obj.get_json())
            except Exception, e:
                print e
            """


class ForeverDreamingParser:
    def __init__(self, season, episode):
        self.season = season
        self.episode = episode

    def parse_html(self, html):
        # Remove Strong Elements from html, to better recognize spoken passages by Regex
        html = html.replace("<strong>", "")
        html = html.replace("</strong>", "")

        # Only process script body
        html = html.split('<hr class="sep" />')[-2]

        parser = MyHTMLParser(self.season, self.episode)
        parser.feed(html)
