from flask import Flask
import os
from dotenv import load_dotenv

from UI.app import UI_BP
from Spell_Checker.CharRNN import CharRNN

dirname = os.path.dirname(__file__)
load_dotenv()

APP = Flask(__name__, template_folder=os.path.join(dirname, 'UI', 'templates'), static_folder=os.path.join(dirname, 'UI', 'static'))
APP.register_blueprint(UI_BP, url_prefix='/')

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

if __name__ == "__main__":

    from os import path, walk

    extra_dirs = [os.path.join(dirname, 'UI', 'templates')]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    APP.run(host=HOST, port=PORT, debug=True, extra_files=extra_files)
