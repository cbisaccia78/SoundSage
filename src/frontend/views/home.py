import random

from flask import render_template, request, Blueprint, Response, redirect

from backend.spotify.playlists import PlaylistManager
from backend.models.rating_predictor import create_rating_model


playlist_manager = None
tracks = None
num_tracks = 0

index = 0

shuffle = False

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=["GET", "POST"])
def home():
    return render_template(
        'home.jinja2',
        playlist_name=None if not playlist_manager else playlist_manager.name,
        track=None if not tracks else tracks[index],
        shuffle=shuffle,
        )

@bp.route('/previous', methods=["GET"])
def previous():

    global index

    index = (index - 1) % num_tracks

    return redirect('/')

@bp.route('/play', methods=["GET"])
def play():

    return redirect('/')

@bp.route('/next', methods=["GET"])
def next():
    global index

    index = (index + 1) % num_tracks

    return redirect('/')

@bp.route('/shuffle', methods=["GET"])
def shuffle():

    global shuffle

    shuffle = not shuffle
    
    if shuffle:
        random.shuffle(tracks)

    return redirect('/')

@bp.route('/submit_ratings', methods=["POST"])
def submit_ratings():
    global tracks

    for key, value in request.form.items():
        if key.startswith("rating-"):
            tracks[index].rating = int(value)  # Store the rating as an integer

    
    return redirect('/')

@bp.route('/import_playlist', methods=['POST'])
def import_playlist():
    global playlist_manager
    global tracks
    global num_tracks

    playlist_id = request.form.get('playlistId')
    # playlist_file = request.files.get('playlistFile')

    # Handle playlist link (from Spotify)
    if playlist_id:
        # Perform actions with the playlist link (e.g., use Spotify API to fetch songs)
        print(f"Received Spotify link: {playlist_id}")
        playlist_manager = PlaylistManager(playlist_id)
        tracks = playlist_manager.get_tracks()
        num_tracks = len(tracks)

    
    """ # Handle file upload (optional)
    if playlist_file:
        # Save and process the uploaded playlist file
        filename = playlist_file.filename
        print(f"Received playlist file: {filename}") """
    
    return redirect('/')

@bp.route('/create_model', methods=["GET"])
def create_model():
    rated_tracks = [track for track in tracks if track.rating is not None]
    model = create_rating_model(rated_tracks)

    return redirect('/')

@bp.route('bing/<int:id>', methods=["GET"])
def bing(id):

    return Response("{}", status=200, content_type="text/plain")