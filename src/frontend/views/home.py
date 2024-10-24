from flask import render_template, request, Blueprint, Response, session


playlist = None

index = 0

shuffle = False

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=["GET", "POST"])
def home():

    global shuffle
    global playlist
    global index

    return render_template('home.jinja2', playlist_name=playlist['name'], song=playlist['songs'][index], shuffle=shuffle)

@bp.route('/previous', methods=["GET"])
def previous():

    global shuffle
    global playlist
    global index

    return render_template('home.jinja2', playlist_name=playlist['name'], song=playlist['songs'][index], shuffle=shuffle)

@bp.route('/play', methods=["GET"])
def play():

    global shuffle
    global playlist
    global index

    return render_template('home.jinja2', playlist_name=playlist['name'], song=playlist['songs'][index], shuffle=shuffle)

@bp.route('/next', methods=["GET"])
def next():

    global shuffle
    global playlist
    global index

    return render_template('home.jinja2', playlist_name=playlist['name'], song=playlist['songs'][index], shuffle=shuffle)

@bp.route('/shuffle', methods=["GET"])
def shuffle():

    global shuffle
    global playlist
    global index

    shuffle = not shuffle

    return render_template('home.jinja2', playlist_name=playlist['name'], song=playlist['songs'][index], shuffle=shuffle)

@bp.route('/import_playlist', methods=['POST'])
def import_playlist():
    playlist_link = request.form.get('playlistLink')
    playlist_file = request.files.get('playlistFile')

    # Handle playlist link (from Spotify)
    if playlist_link:
        # Perform actions with the playlist link (e.g., use Spotify API to fetch songs)
        print(f"Received Spotify link: {playlist_link}")
    
    # Handle file upload (optional)
    if playlist_file:
        # Save and process the uploaded playlist file
        filename = playlist_file.filename
        print(f"Received playlist file: {filename}")
    
    return render_template('home.jinja2', playlist=playlist)

@bp.route('bing/<int:id>', methods=["GET"])
def bing(id):

    return Response("{}", status=200, content_type="text/plain")