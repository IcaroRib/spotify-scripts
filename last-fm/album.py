from difflib import SequenceMatcher
import re

class Album:

    def __init__(self, name, play_count, artist, id):
        self.name = name
        self.artist = artist
        self.play_count = play_count
        self.mbid = id

    def get_key(self):
        if self.mbid is None or self.mbid == "":
            return self.name
        return self.mbid

    def max_similar(self, other_albums):
        max_match = 0
        key = None
        name_key = None
        for o in other_albums:
            a = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", self.name)
            b = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", o.name)
            match = SequenceMatcher(None, a, b).ratio()
            if match > max_match:
                max_match = match
                name_key = o.name
                key = o.get_key()
        if max_match > 0.7:
            if max_match < 1:
                print(f"Match: {self.get_key()} xxxx {name_key}: {max_match}")
            return key
        return self.get_key()

    def print(self, i):
        return f"{i}. {self.name} - {self.artist}: {self.play_count}"