import re
from HTMLParser import HTMLParser
import keywords as k
from MongoDB.MongoDBConnection import MongoDBConnection
from Parser.TvShowModel import Replik


class MyHTMLParser(HTMLParser):

    def __init__(self, season, episode):
        HTMLParser.__init__(self)
        self.season = season
        self.episode = episode
        self.mongo_db = MongoDBConnection()
        self.out = {"1": []}
        self.scene_count = 0
        self.con = self.mongo_db.get_con()
        self.db = self.mongo_db.get_db_by_name(k.BIG_BANG_THEORY)
        self.replik_coll = self.mongo_db.get_coll_by_db_and_name(k.BIG_BANG_THEORY, k.REPLIK_COLLECTION)

    def handle_data(self, data):
        #print "Encountered some data  :", data
        re_spoken = re.compile(r'[A-Z]{1}[a-z]+\s?(\([\sA-Za-z0-9]*\))?:')
        re_alpha_numeric = re.compile('[^a-zA-Z\s]')
        re_quotation_marks = re.compile(
            ur'[\u0022\u0027\u00AB\u00BB\u2018\u2019\u201A\u201B\u201C\u201D\u201E\u201F\u2039\u203A\u300C\u300D\u300E\u300F\u301D\u301E\u301F\uFE41\uFE42\uFE43\uFE44\uFF02\uFF07\uFF62\uFF63]+')

        if data.startswith("Scene:") or data.startswith("</hr>"):
            if "%s" % self.scene_count not in self.out:
                self.out["%s" % self.scene_count] = []
            self.scene_count += 1
            if "%s" % self.scene_count not in self.out:
                self.out["%s" % self.scene_count] = []
            return

        if re.search(re_spoken, data) is not None:

            try:
                speaker, replik = data.split(':', 1)
            except Exception, e:
                print e
                return

            speaker = re.sub("\(.*", "", speaker.decode('utf-8'))
            replik = replik.decode('utf-8')
            replik = re.sub(re_quotation_marks, "", replik)
            replik = re.sub(re_alpha_numeric, "", replik)

            replik_word_count = len(replik.split())

            new_replik = Replik()
            new_replik._speaker = speaker
            new_replik._replik = replik
            new_replik._replik_word_count = replik_word_count
            new_replik._scene_number = self.scene_count
            new_replik._episode_number = self.episode
            new_replik._season_number = self.season

            self.out["%s" % self.scene_count].append(new_replik)
            self.replik_coll.insert(new_replik.get_json())


class ForeverDreamingParser():

    def __init__(self, season, episode):
        self.season = season
        self.episode = episode

    def parse_html(self, html):

        html = html.replace("<strong>", "")
        html = html.replace("</strong>", "")
        html = html.split('<hr class="sep" />')[-2]

        parser = MyHTMLParser(self.season, self.episode)
        parser.feed(html)

        scenes = parser.out

        return scenes