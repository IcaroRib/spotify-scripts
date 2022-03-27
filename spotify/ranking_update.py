from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def get_oath_client(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDICT_URI):
    scope = "playlist-read-collaborative,playlist-modify-public,playlist-modify-private,playlist-read-private"
    auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                 redirect_uri=SPOTIPY_REDICT_URI,scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def get_last_date(sp, GLOBAL_PLAYLIST):
    global_playlist_results = sp.playlist(playlist_id=GLOBAL_PLAYLIST,fields='tracks')['tracks']
    tracks_global = []
    c = 0
    for k in global_playlist_results:
            tracks = global_playlist_results[k]
            c+=1
            if c > 1:
                break
    last_date = tracks[0]['added_at']
    
    return last_date

def get_top_songs_uri(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, last_date):

    countries_uri = ['37i9dQZEVXbMH2jvi6jvjk?si=e3911437648b48c1',
                 'https://open.spotify.com/playlist/37i9dQZEVXbJiZcmkrIHGU?si=5a29583fa8e34b23',
                 'https://open.spotify.com/playlist/37i9dQZEVXbLrQBcXqUtaC?si=35ff2e9724094a73',
                 'https://open.spotify.com/playlist/37i9dQZEVXbMMy2roB9myp?si=17009d80233b4023',
                 'https://open.spotify.com/playlist/37i9dQZEVXbJPcfkRz0wJ0?si=be0c06774e524121'    
                 ]
    
    credentials = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)
    songs_uri = []
    
    for country_uri in countries_uri:
        results = spotify.playlist(playlist_id=country_uri,fields='tracks')
        dict_results = results['tracks']
        tracks = []
        c = 0 
        for k in dict_results:
            tracks = dict_results[k]
            c+=1
            if c > 1:
                break

        first_track = tracks[0]
        date = first_track['added_at']
        if date > last_date:
            update_playlist = False
            break
        song_uri = first_track['track']['uri']
        song_name = first_track['track']['name']
        if song_uri not in songs_uri:
            print(f"Song to add... {song_name} - {song_uri}")
            songs_uri.append(song_uri)    

    return songs_uri


def check_and_update_playlist():

    print('Starting the update...')
    
    SPOTIPY_CLIENT_ID = '2a91de2dd32d4cb0ad343343d8c5661d'
    SPOTIPY_CLIENT_SECRET = '99b2d7fce23d48368be875276606f5bd'
    SPOTIPY_REDICT_URI = 'http://localhost'
    GLOBAL_PLAYLIST = 'https://open.spotify.com/playlist/6xXpdSXNWj0QqXrTQhNrp0?si=38ab169970e04c51'

    sp = get_oath_client(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDICT_URI)
    print('Oath Client check. Proceed')
    last_date = get_last_date(sp, GLOBAL_PLAYLIST)
    songs_uri = get_top_songs_uri(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, last_date) 
    if len(songs_uri) == 0:
        print('No songs to update...')
        return
    sp.playlist_replace_items(GLOBAL_PLAYLIST, songs_uri)
    print('Update sucessfull,..')

app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
sched.add_job(check_and_update_playlist, 'interval',minutes=60)
sched.start()

if __name__ == "__main__":
    app.run()
