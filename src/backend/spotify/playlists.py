import requests
import sys
import os

class PlaylistManager:
    def __init__(self, playlist_id=None):
        self.playlist_id = playlist_id
        if playlist_id is not None:
            self.load_playlist(playlist_id)

    def load_playlist(self,playlist_id, fields="name,images,tracks(items(track(name,id,album(name,images),artists(name)))"):
        # Define the base URL for the playlist info request
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        
        # Append fields to the URL if provided
        if fields:
            url += f"?fields={fields}"
        
        # Set the headers, including the Authorization Bearer token
        headers = {
            "Authorization": f"Bearer {os.environ['access_token']}"
        }
        
        # Make the GET request to retrieve playlist information
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response and return playlist info
            self.playlist = response.json()
        else:
            # Print the error response for debugging
            print(f"Error: {response.status_code}, {response.text}")
            raise RuntimeError("")
        
    @property
    def name(self):
        return self.playlist['name']
    
    def get_tracks(self):
        return [Track(track['track']) for track in self.playlist['tracks']['items']]
    
class Track:
    def __init__(self, track_dict):
        self.name = track_dict['name']
        self.id = track_dict['id']
        self.artists = [artist['name'] for artist in track_dict['artists']]
        self.album_name = track_dict['album']['name']
        self.album_images = track_dict['album']['images']
        self.audio_features = None
        self.audio_analysis = None
        self.rating = None
    
    def load_audio_features(self):
        # Define the base URL for the playlist info request
        url = f"https://api.spotify.com/v1/audio-features/{self.id}"
        
        # Set the headers, including the Authorization Bearer token
        headers = {
            "Authorization": f"Bearer {os.environ['access_token']}"
        }
        
        # Make the GET request to retrieve playlist information
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response and return playlist info
            resp = response.json()

            del resp['track_href']
            del resp['uri']
            del resp['type']
            del resp['analysis_url']
            del resp['id']

            self.audio_features = resp
        else:
            # Print the error response for debugging
            print(f"Error: {response.status_code}, {response.text}")
            raise RuntimeError("")

    def load_audio_analysis(self):
        # Define the base URL for the playlist info request
        url = f"https://api.spotify.com/v1/audio-analysis/{self.id}"
        
        # Set the headers, including the Authorization Bearer token
        headers = {
            "Authorization": f"Bearer {os.environ['access_token']}"
        }
        
        # Make the GET request to retrieve playlist information
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response and return playlist info
            resp = response.json()

            del resp['meta']

            track = resp['track']
            del track['sample_md5']
            del track['codestring']
            del track['code_version']
            del track['echoprintstring']
            del track['echoprint_version']
            del track['synchstring']
            del track['synch_version']
            del track['rhythmstring']
            del track['rhythm_version']

            self.audio_analysis = resp
        else:
            # Print the error response for debugging
            print(f"Error: {response.status_code}, {response.text}")
            raise RuntimeError("")

    
if __name__ == '__main__':
    import os
    import authentication

    from ml_utils.transformations import flatten_dict_values

    id = os.environ['SPOTIFY_CLIENT_ID']
    secret = os.environ['SPOTIFY_CLIENT_SECRET']

    os.environ['access_token'] = authentication.get_access_token(id, secret)

    av = sys.argv
    playlist_id = av[1]
    pm = PlaylistManager()
    pm.load_playlist(playlist_id)
    print(list(pm.playlist.keys()))
    track = pm.get_tracks()[0]
    print(track.name)
    print(track.id)
    track.load_audio_analysis()
    track.load_audio_features()
    print(flatten_dict_values(track.audio_analysis))
    print(flatten_dict_values(track.audio_features))
    