import requests
import sys

from flask import session

class PlaylistManager:
    def __init__(self, playlist_id=None):
        self.playlist_id = playlist_id
        if playlist_id is not None:
            self.load_playlist(playlist_id)

    def load_playlist(self,playlist_id, fields=None):
        # Define the base URL for the playlist info request
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        
        # Append fields to the URL if provided
        if fields:
            url += f"?fields={fields}"
        
        # Set the headers, including the Authorization Bearer token
        headers = {
            "Authorization": f"Bearer {session.get('access_token')}"
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
    
if __name__ == '__main__':
    import os
    import authentication

    id = os.environ['SPOTIFY_CLIENT_ID']
    secret = os.environ['SPOTIFY_CLIENT_SECRET']

    session['access_token'] = authentication.get_access_token(id, secret)

    av = sys.argv
    at = av[1]
    playlist_id = av[2]
    pm = PlaylistManager()
    pm.load_playlist(playlist_id, "name,images,tracks(items(track(name,album(name,images),artists(name)))")
    print(list(pm.playlist.keys()))
    tracks = pm.playlist['tracks']['items']