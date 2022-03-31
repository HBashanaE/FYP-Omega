from flask import Flask
import os
from dotenv import load_dotenv

from UI.app import UI_BP
from Spell_Checker.CharRNN import CharRNN

dirname = os.path.dirname(__file__)
load_dotenv()

APP = Flask(__name__, template_folder=os.path.join(dirname, 'UI', 'templates'))
APP.register_blueprint(UI_BP, url_prefix='/')

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

if __name__ == "__main__":
    APP.run(host=HOST, port=PORT, debug=True)
