import os
from HTMLParser import HTMLParser
from MongoDB.MongoDBConnection import MongoDBConnection
from Parser.models.Replik import Replik
import glob
import keywords as k
import re
import regex
import requests


class LOSTHTMLParser(HTMLParser):
    def __init__(self, season, episode, scene):
        HTMLParser.__init__(self)

        self.mongo_db = MongoDBConnection()

        self.con = self.mongo_db.get_con()
        self.db = self.mongo_db.get_db_by_name(k.LOST)
        self.episode = episode
        self.out = {"0": []}
        self.scene = scene
        self.replik_coll = self.mongo_db.get_coll_by_db_and_name(k.LOST, k.REPLIK_COLLECTION)
        self.scene_coll = self.mongo_db.get_coll_by_db_and_name(k.LOST, k.SCENE_COLLECTION)
        self.speaker_coll = self.mongo_db.get_coll_by_db_and_name(k.LOST, k.SPEAKER_COLLECTION)
        self.scene_count = 0
        self.replik_count = 0
        self.season = season
        self.replik_list = []

    def handle_data(self, data):

        data = data.replace('\n', '').replace('\t', '').replace('\\', '').rstrip()

        re_spoken = re.compile(ur'[A-Z]+:')  # Regex to find repliks
        re_alpha_numeric = regex.compile('^a-zA-Z\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}\s', regex.UNICODE)  # Regex to remove non alpha numeric characters
        re_annotations = re.compile(r'\[[\w \(\)]*\]')
        re_quotation_marks = re.compile(
            ur'[\u0022\u0027\u00AB\u00BB\u2018\u2019\u201A\u201B\u201C\u201D\u201E\u201F\u2039'
            ur'\u203A\u300C\u300D\u300E\u300F\u301D\u301E\u301F\uFE41\uFE42\uFE43\uFE44\uFF02\uFF07\uFF62\uFF63]+')

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
            speaker = speaker.strip().lower()
            replik = replik.decode('utf-8')
            replik = re.sub(re_quotation_marks, "", replik)
            replik = re.sub(re_annotations, "", replik)
            replik = regex.sub(re_alpha_numeric, "", replik)

            replik_word_count = len(replik.split())

            # Initiate new Replik object and insert in MongoDB
            new_replik = Replik()
            new_replik._speaker = speaker
            new_replik._replik = replik
            new_replik._replik_word_count = replik_word_count
            new_replik._scene_number = self.scene
            new_replik._episode_number = self.episode
            new_replik._season_number = self.season
            new_replik._replik_number = self.replik_count

            self.replik_count += 1
            self.replik_list.append(new_replik.get_json())


class LOSTParser:
    def __init__(self, season, episode):
        self.season = int(season)
        self.episode = int(episode)

    def parse_html(self, html):
        # Remove Strong Elements from html, to better recognize spoken passages by Regex
        html = html.replace("<strong>", "")
        html = html.replace("</strong>", "")

        scene_list = []
        re_quotation_marks = re.compile(
            ur'[\u0022\u0027\u00AB\u00BB\u2018\u2019\u201A\u201B\u201C\u201D\u201E\u201F\u2039'
            ur'\u203A\u300C\u300D\u300E\u300F\u301D\u301E\u301F\uFE41\uFE42\uFE43\uFE44\uFF02\uFF07\uFF62\uFF63]+')

        html = re.split(r'<h2><span class="mw-headline" id="Act_[0-9]?">Act [0-9]?</span></h2>|<h2><span class="mw-headline" id="Part_[0-9]?">Part [0-9]?</span></h2>', html)
        for act in html:
            for scene in re.split(r'<hr>', act):
                sc_without_quot_marks = re.sub(re_quotation_marks, "", scene)
                if re.match(r'\s?[\s]*<p>\[[A-Z]?[\s\w.\-,;?!]*\]\s*</p>', sc_without_quot_marks):
                    scene_list.append(scene)

        for id, scene in enumerate(scene_list):
            parser = LOSTHTMLParser(self.season, self.episode, id+1)
            parser.feed(scene)

            for replik in parser.replik_list:
                requests.post("http://localhost:8080/post_replik", json=replik,
                          headers={"content-type": "application/json"})

def log(string):
    print "### " + string

if __name__ == "__main__":

    # Read paths of html files in download folder
    log("Open HTML Files")

    for html_f in os.listdir("data/lost"):
        if not html_f.startswith("."):
            with open("data/lost/%s" % html_f, "r") as f:
                season_number, episode_number, title = html_f.split("_")

                html = f.read()

                # Regex for extracting Season and Episode number
                re_season_episode = re.compile(r'[0-9]+x[0-9]+')

                #season_episode = re.search(re_season_episode, html).group(0)
                #season_number, episode_number = (int(i) for i in season_episode.split('x'))

                log("Parsing Season %s Episode %s" % (season_number, episode_number))

                # Parse Episode HTML, saves Repliks and Scenes to MongoDB
                try:
                    parser = LOSTParser(season_number, episode_number)
                    parser.parse_html(html)
                except Exception, e:
                    log("Could not parse Season %s Episode %s" % (season_number, episode_number))
                    log("Reason: %s" % e.message)

                log("Succesfully parsed Season %s Episode %s" % (season_number, episode_number))
