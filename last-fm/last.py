import requests
from artist import Artist
from song import Song
from album import Album

class Crawller:

    METHODS = ["user.getTopArtists", "user.getTopTracks", "user.getTopAlbums"]
    BASE_URL = "https://ws.audioscrobbler.com/2.0/?method={method}&user={user}" \
               "&period={period}&api_key={key}&format=json&limit={limit}&page={page}"
    PERIOD = "overall"
    LIMIT = 1000

    TAGS = {
        "artists": ("topartists", "artist"),
        "albums": ("topalbums", "album"),
        "songs": ("toptracks", "track")
    }

    def __init__(self, key):
        self.api_key = key

    def aggregate(self, elements):
        dic = {}
        for a in elements:
            if a.get_key() in dic:
                dic[a.get_key()].play_count += a.play_count
            elif type(a) == Album and (a.mbid is None or a.mbid == ""):
                copy = list(elements)
                filtered_albums = list(filter(lambda e: (e.artist == a.artist), copy))
                filtered_albums.remove(a)
                max_similar = a.max_similar(filtered_albums)
                if max_similar in dic:
                    dic[max_similar].play_count += a.play_count
                else:
                    dic[a.get_key()] = a
            else:
                dic[a.get_key()] = a
        return dic

    def sort(self, elements):
        return {k: v for k, v in sorted(elements.items(), reverse=True, key=lambda item: item[1].play_count)}

    def get_artists_list(self, users):
        artists = []
        for u in users:
            artists.extend(self.get_list(Crawller.METHODS[0], u, Crawller.TAGS["artists"]))
        return self.sort(self.aggregate(artists))

    def get_songs_list(self, users):
        songs = []
        for u in users:
            songs.extend(self.get_list(Crawller.METHODS[1], u, Crawller.TAGS["songs"]))
        return self.sort(self.aggregate(songs))

    def get_albums_list(self, users):
        albums = []
        for u in users:
            albums.extend(self.get_list(Crawller.METHODS[2], u, Crawller.TAGS["albums"]))
        return self.sort(self.aggregate(albums))

    def get_list(self, method, user, tags):
        formatted_url = Crawller.BASE_URL.format(user=user, method=method,
                                                 period=Crawller.PERIOD, key=self.api_key,
                                                 limit = Crawller.LIMIT, page=1)

        main_tag = tags[0]
        second_tag = tags[1]

        req = requests.get(formatted_url)
        content = req.json()[main_tag]
        list_content = Crawller.map(method, content[second_tag])
        max_pages = int(content["@attr"]["totalPages"])

        for p in range(2, max_pages):
            formatted_url = Crawller.BASE_URL.format(user=user, method=method,
                                                     period=Crawller.PERIOD, key=self.api_key,
                                                     limit=Crawller.LIMIT, page=p)
            req = requests.get(formatted_url)
            content = req.json()[main_tag]
            list_content.extend(Crawller.map(method, content[second_tag]))

        return list_content

    @staticmethod
    def map(method, content):
        if method == Crawller.METHODS[0]:
            return Crawller.map_artists(content)
        elif method == Crawller.METHODS[1]:
            return Crawller.map_songs(content)
        elif method == Crawller.METHODS[2]:
            return Crawller.map_albums(content)

    @staticmethod
    def map_artists(artists):
        list_artists = []
        for a in artists:
            new_artist = Artist(a["name"], int(a["playcount"]), a["mbid"])
            list_artists.append(new_artist)
        return list_artists

    @staticmethod
    def map_songs(songs):
        list_songs = []
        for s in songs:
            new_song = Song(s["name"], int(s["playcount"]), s["artist"]["name"], s["mbid"])
            list_songs.append(new_song)
        return list_songs

    @staticmethod
    def map_albums(albums):
        list_albums = []
        for a in albums:
            new_album = Album(a["name"], int(a["playcount"]), a["artist"]["name"], a["mbid"])
            list_albums.append(new_album)
        return list_albums

    @staticmethod
    def print(content):
        listed_content = list(content.values())
        for i in range(0, len(content)):
            e = listed_content[i]
            print(e.print(i+1))

    @staticmethod
    def write(content, filename):
        with open(filename, "w", encoding="utf-8") as file:
            listed_content = list(content.values())
            for i in range(0, len(content)):
                e = listed_content[i]
                file.write(e.print(i + 1)+"\n")



mau = ["castro-san", "MM_1", "Mauricio_senju", "Shiver_1", "former_junkie", "irvine_1", "kohler_1", "MCL_1", "abraxas_1", "msjenkins_"]
key = "cf5d63aab87dc7571432fd6bbc862298"
c = Crawller(key)

#artists = c.get_artists_list(mau)
#Crawller.write(artists, "mau_artists.txt")

albums = c.get_albums_list(mau)
Crawller.write(albums, "mau_albums_v2.txt")

#songs = c.get_songs_list(mau)
#Crawller.write(songs, "mau_songs.txt")