import requests
import sys


def get_access_token(client_id, client_secret):
    # Define the URL for the token request
    url = "https://accounts.spotify.com/api/token"
    
    # Set the headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Set the data for the request
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    # Make the POST request to get the access token
    response = requests.post(url, headers=headers, data=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and return the access token
        return response.json().get("access_token")
    else:
        # Print the error response for debugging
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
if __name__ == '__main__':
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    access_token = get_access_token(client_id, client_secret)
    print(access_token)