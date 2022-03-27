class Song:

    def __init__(self, name, play_count, artist, id):
        self.name = name
        self.mbid = id
        self.artist = artist
        self.play_count = play_count

    def get_key(self):
        if self.mbid is None or self.mbid == "":
            return (self.name, self.artist)
        return self.mbid

    def print(self, i):
        return f"{i}. {self.name} - {self.artist}: {self.play_count}"