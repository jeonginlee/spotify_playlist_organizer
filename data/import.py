import os
from contextlib import contextmanager
import sys
# adding directory to import database connection
sys.path.insert(0, "../model")

from database import SpotifyDB

# --------------------------------------------
# Helper class for reading files
class FileReader(object):
    def __init__(self, filename):
        self.filename = filename

    @contextmanager
    def openFile(self):
        try:
            file = open(self.filename, "r", encoding = "utf8")
            yield file
        finally:
            file.close()

def importTracks():
    reader = FileReader("tracks.csv")
    with reader.openFile() as file:
        lines = file.read().splitlines()
        for line in lines:
            print(line)
            line = line.split(';')

            acousticness, analysis_url , danceability, duration_ms, energy, Id, instrumentalness, music_key, liveness, loudness, mode, name, speechiness, tempo, time_signature, track_href, TYPE, uri, valence = line


            print(name)


if __name__ == "__main__":


    files = os.listdir()
    files = [x for x in files if ".csv" in x]
    print(files)

    db = SpotifyDB()

    importTracks()

