import os
import json
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
            yield json.load(file)
        finally:
            file.close()

def importHelper(filename, func):
    reader = FileReader(filename)
    with reader.openFile() as data:
        print(f"Reading {filename}")
        for entry in data:
            func(entry)

if __name__ == "__main__":
    files = os.listdir()
    files = [x for x in files if x.endswith(".json")]

    db = SpotifyDB()

    print("Take a lap, this will take about a minute or two.")

    # Call function depending on file
    for file in files:
        table = file.split(".")[0]
        tables = ["tracks", "artists", "genres", "artistToGenre", "trackToGenre"]
        if table in tables:
            func = getattr(db, f"{table}Import")
            importHelper(file, func)
        else:
            print(table)
            raise Exception(f"Filename {file} invalid.")

    print("Import complete.")
