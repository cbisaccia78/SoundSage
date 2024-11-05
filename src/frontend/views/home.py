from flask import render_template, request, Blueprint, Response, redirect, url_for

from backend.spotify.playlists import PlaylistManager


playlist = None

index = 0

shuffle = False

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=["GET", "POST"])
def home():

    global shuffle
    global playlist_manager
    global index

    return render_template('home.jinja2', playlist_name=None if not playlist_manager else playlist_manager.name, song=None if not playlist_manager else playlist_manager['songs'][index], shuffle=shuffle)

@bp.route('/previous', methods=["GET"])
def previous():

    global shuffle
    global playlist_manager
    global index

    return redirect(url_for('static'))

@bp.route('/play', methods=["GET"])
def play():

    global shuffle
    global playlist_manager
    global index

    return render_template('home.jinja2', playlist_name=None if not playlist_manager else playlist_manager.name, song=None if not playlist_manager else playlist_manager['songs'][index], shuffle=shuffle)

@bp.route('/next', methods=["GET"])
def next():

    global shuffle
    global playlist_manager
    global index

    return render_template('home.jinja2', playlist_name=None if not playlist_manager else playlist_manager.name, song=None if not playlist_manager else playlist_manager['songs'][index], shuffle=shuffle)

@bp.route('/shuffle', methods=["GET"])
def shuffle():

    global shuffle
    global playlist_manager
    global index

    shuffle = not shuffle

    return render_template('home.jinja2', playlist_name=None if not playlist_manager else playlist_manager.name, song=None if not playlist_manager else playlist_manager['songs'][index], shuffle=shuffle)

@bp.route('/import_playlist', methods=['POST'])
def import_playlist():
    global shuffle
    global playlist_manager
    global index

    playlist_id = request.form.get('playlistId')
    # playlist_file = request.files.get('playlistFile')

    # Handle playlist link (from Spotify)
    if playlist_id:
        # Perform actions with the playlist link (e.g., use Spotify API to fetch songs)
        print(f"Received Spotify link: {playlist_id}")
        playlist_manager = PlaylistManager(playlist_id)

    
    """ # Handle file upload (optional)
    if playlist_file:
        # Save and process the uploaded playlist file
        filename = playlist_file.filename
        print(f"Received playlist file: {filename}") """
    
    return render_template('home.jinja2', playlist_name=None if not playlist_manager else playlist_manager.name, song=None if not playlist_manager else playlist_manager.get_tracks()[index].name, shuffle=shuffle)

@bp.route('bing/<int:id>', methods=["GET"])
def bing(id):

    return Response("{}", status=200, content_type="text/plain")