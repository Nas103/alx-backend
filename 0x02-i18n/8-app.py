#!/usr/bin/env python3
"""Flask app to demonstrate locale and timezone selection with user preferences."""

from flask import Flask, request, render_template, g
from flask_babel import Babel, format_datetime
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

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
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    
    user = getattr(g, 'user', None)
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']
    
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    """Determine the best match for supported timezones."""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone)
        except UnknownTimeZoneError:
            pass
    
    user = getattr(g, 'user', None)
    if user:
        try:
            return pytz.timezone(user['timezone'])
        except UnknownTimeZoneError:
            pass
    
    return pytz.timezone('UTC')


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
    current_time = format_datetime(datetime.now(), tzinfo=get_timezone())
    return render_template('index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(debug=True)
