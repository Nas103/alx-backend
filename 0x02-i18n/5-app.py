#!/usr/bin/env python3
"""Flask app to demonstrate mock login and locale selection."""

from flask import Flask, request, render_template, g
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

LANGUAGES = {
    'en': 'English',
    'fr': 'French'
}

app.config['LANGUAGES'] = LANGUAGES


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    user = getattr(g, 'user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


def get_user():
    """Retrieve a user by ID."""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set the user in the global context before each request."""
    g.user = get_user()


@app.route('/')
def index():
    """Render the index page."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
