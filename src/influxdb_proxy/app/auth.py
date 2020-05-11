
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from ..app import app


auth = HTTPBasicAuth()

users = {
    app.config['AUTH_USER']: generate_password_hash(app.config['AUTH_PASS']),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(
        users.get(username), password
    ):
        return username
