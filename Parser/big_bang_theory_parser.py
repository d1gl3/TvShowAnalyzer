import glob

import re

from BigBangTheoryParser import BigBangTheoryParser as Parser


def log(string):
    print "### " + string


if __name__ == "__main__":

    # Read paths of html files in download folder
    log("Open HTML Files")

    raw_html_files = glob.glob('data/*.html')  # ["data/raw_html_10.html"]
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
                parser = Parser(season_number, episode_number)
                parser.parse_html(html)
            except Exception, e:
                log("Could not parse Season %s Episode %s" % (season_number, episode_number))
                log("Reason: %s" % e.message)

            log("Succesfully parsed Season %s Episode %s" % (season_number, episode_number))