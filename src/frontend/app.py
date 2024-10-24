import datetime

from flask import Flask

from frontend.views import home

app = Flask(__name__)

app.secret_key = b'2da61be40a82b889f67934a58a490a325155e5eaf470e2a59e1965bcb496d00c'

app.register_blueprint(home.bp)

@app.context_processor
def inject_year():
    return {'current_year': datetime.datetime.utcnow().year}