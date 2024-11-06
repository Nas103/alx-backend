#!/usr/bin/env python3
"""Flask app to demonstrate locale selection via URL parameter."""

from flask import Flask, request, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

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
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/')
def index():
    """Render the index page."""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
