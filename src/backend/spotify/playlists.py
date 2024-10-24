import requests
import sys

def get_playlist(access_token, playlist_id, fields=None):
    # Define the base URL for the playlist info request
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    
    # Append fields to the URL if provided
    if fields:
        url += f"?fields={fields}"
    
    # Set the headers, including the Authorization Bearer token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Make the GET request to retrieve playlist information
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and return playlist info
        return response.json()
    else:
        # Print the error response for debugging
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
if __name__ == '__main__':
    av = sys.argv
    at = av[1]
    playlist_id = av[2]
    playlist = get_playlist(at, playlist_id, "name,images,tracks(items(track(name,album(name,images),artists(name)))")
    print(list(playlist.keys()))
    tracks = playlist['tracks']['items']
    
    #print([track['name'] for track in playlist['tracks']])