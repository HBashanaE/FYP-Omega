from flask import Flask
import os

from UI.app import UI_BP
from Spell_Checker.CharRNN import CharRNN

dirname = os.path.dirname(__file__)

APP = Flask(__name__, template_folder=os.path.join(dirname, 'UI', 'templates'))

APP.register_blueprint(UI_BP, url_prefix='/')

if __name__ == "__main__":
    APP.run(port=4000, debug=True)
