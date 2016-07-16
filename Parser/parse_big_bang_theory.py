import glob
import re
from ForeverDreamingParser import ForeverDreamingParser as Parser


def parse_big_bang_theory_raw_html_to_repliks():
    raw_html_files = glob.glob('data/*.html')
    for html in raw_html_files:
        with open(html, "r") as f:
            html = f.read()

            re_season_episode = re.compile(r'[0-9]+x[0-9]+')

            season, episode = re.search(re_season_episode, html).group(0).split('x')

            parser = Parser(season, episode)
            episode_scenes = parser.parse_html(html)
            del episode_scenes['0']

            print episode_scenes

def calculate_scene_stats():
    pass

if __name__ == "__main__":
    parse_big_bang_theory_raw_html_to_repliks()
