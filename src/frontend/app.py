import datetime
import os

from flask import Flask

from frontend.views import home
from backend.spotify.authentication import get_access_token

app = Flask(__name__)

app.secret_key = b'2da61be40a82b889f67934a58a490a325155e5eaf470e2a59e1965bcb496d00c'

id = os.environ['SPOTIFY_CLIENT_ID']
secret = os.environ['SPOTIFY_CLIENT_SECRET']

os.environ['access_token'] = get_access_token(id, secret)

app.register_blueprint(home.bp)

@app.context_processor
def inject_year():
    return {'current_year': datetime.datetime.utcnow().year}