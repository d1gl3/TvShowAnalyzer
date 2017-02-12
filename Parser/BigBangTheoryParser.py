from HTMLParser import HTMLParser
from MongoDB.MongoDBConnection import MongoDBConnection
from Parser.models.Replik import Replik
import glob
import keywords as k
import re
import requests

from Parser.models.Scene import Scene
from name_mapping import name_mapping, filtered_names


class BigBangHTMLParser(HTMLParser):
    def __init__(self, season, episode, title):
        HTMLParser.__init__(self)

        self.mongo_db = MongoDBConnection()

        self.con = self.mongo_db.get_con()
        self.db = self.mongo_db.get_db_by_name("bbt_new")
        self.episode = episode
        self.out = {"0": []}
        self.replik_coll = self.mongo_db.get_coll_by_db_and_name("bbt_new", k.REPLIK_COLLECTION)
        self.scene_coll = self.mongo_db.get_coll_by_db_and_name("bbt_new", k.SCENE_COLLECTION)
        self.speaker_coll = self.mongo_db.get_coll_by_db_and_name("bbt_new", k.SPEAKER_COLLECTION)
        self.transkript_coll = self.mongo_db.get_coll_by_db_and_name("bbt_new", k.TRANSKRIPT_COLLECTION)
        self.scene_count = 0
        self.replik_count = 0
        self.season = season
        self.replik_list = []
        self.transkript = ""
        self.speakers = []
        self.title = title

    def handle_data(self, data):

        data = data.strip()

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

            return

        # Analyze Repliks
        if re.search(re_spoken, data) is not None:

            # Try to split Speaker name from Replik value
            try:
                speakers, replik = data.split(':', 1)
                speakers = re.sub("\(.*", "", speakers.decode('utf-8'))
                speakers = speakers.strip()
            except Exception, e:
                print e
                return

            if speakers == "Scene":
                return

            if speakers in filtered_names:
                pass

            mapped_name = name_mapping.get(speakers)

            if mapped_name:
                if isinstance(mapped_name, list):
                    speakers = mapped_name
                else:
                    speakers = [mapped_name]
            else:
                speakers = [speakers]

            for speaker in speakers:
                # Strip all unwanted characters from Speaker and Replik Value
                replik = replik.decode('utf-8')
                replik = re.sub(re_quotation_marks, "", replik)
                replik = re.sub(re_alpha_numeric, "", replik)

                replik_word_count = len(replik.split())

                if replik_word_count == 0:
                    return

                # Collect speaker names for transkript object
                if speaker not in self.speakers:
                    self.speakers.append(speaker)

                # Initiate new Replik object and insert in MongoDB
                new_replik = Replik()
                new_replik._speaker = speaker
                new_replik._replik = replik
                new_replik._replik_word_count = replik_word_count
                new_replik._scene_number = self.scene_count
                new_replik._episode_number = self.episode
                new_replik._season_number = self.season
                new_replik._replik_number = self.replik_count

                if speaker not in filtered_names:
                    self.replik_list.append(new_replik.get_json())

            self.replik_count += 1
            self.transkript += (data + '\n')


class BigBangTheoryParser:
    def __init__(self, season, episode, title):
        self.season = season
        self.episode = episode
        self.title = title

    def parse_html(self, html):
        # Remove Strong Elements from html, to better recognize spoken passages by Regex
        html = html.replace("<strong>", "")
        html = html.replace("</strong>", "")

        # Only process script body
        html = html.split('<hr class="sep" />')[-2]

        parser = BigBangHTMLParser(self.season, self.episode, self.title)
        parser.feed(html)

        transkript = {
            'content': parser.transkript,
            k.SEASON_NUMBER: parser.season,
            k.EPISODE_NUMBER: parser.episode,
            k.NUMBER_OF_REPLICAS: parser.replik_count,
            k.NUMBER_OF_SCENES: parser.scene_count,
            k.SPEAKERS: parser.speakers,
            k.TITLE: parser.title,
            '_id': 'transkript_%s_%s' % (parser.season, parser.episode)
        }

        parser.transkript_coll.insert(transkript)
        requests.post("http://localhost:8080/api/post_replik", json=parser.replik_list,
                      headers={"content-type": "application/json"})


def log(string):
    print "### " + string


if __name__ == "__main__":

    # Read paths of html files in download folder
    log("Open HTML Files")

    raw_html_files = glob.glob('data/*.html')  # ["data/raw_html_131.html"] #
    for html in raw_html_files:
        with open(html, "r") as f:
            html = f.read()

            # Regex for extracting Season and Episode number
            re_season_episode = re.compile(r'[0-9]+x[0-9]+')

            season_episode = re.search(re_season_episode, html).group(0)
            season_number, episode_number = (int(i) for i in season_episode.split('x'))

            log("Parsing Season %s Episode %s" % (season_number, episode_number))

            # Parse Episode HTML, saves Repliks and Scenes to MongoDB
            try:
                parser = BigBangTheoryParser(season_number, episode_number)
                parser.parse_html(html)
            except Exception, e:
                log("Could not parse Season %s Episode %s" % (season_number, episode_number))
                log("Reason: %s" % e.message)

            log("Succesfully parsed Season %s Episode %s" % (season_number, episode_number))
