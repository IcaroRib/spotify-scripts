class Artist:

    def __init__(self, name, play_count, id):
        self.name = name
        self.mbid = id
        self.play_count = play_count

    def get_key(self):
        if self.mbid is None or self.mbid == "":
            return self.name
        return self.mbid

    def print(self, i):
        return f"{i}. {self.name}: {self.play_count}"
