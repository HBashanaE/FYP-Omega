from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
import os

from Spell_Checker.CharRNN import CharRNN
from Spell_Checker.spellchecker import SpellChecker

UI_BP = Blueprint('UI_BP', __name__)


@UI_BP.route('/', methods=['GET', 'POST'])
def index():
    # return "<p>Hello, World!</p>"
    return render_template('index.html', name='Bashana')


@UI_BP.route('/spellcorrect/', methods=('GET', 'POST'))
def spellcorrect():
    dirname = os.path.dirname(__file__)
    dictionaryPath = os.path.join(
        dirname, '../Data/Names/combined all names - dictionary - train.json')
    neuralModelPath = os.path.join(
        dirname, '../Language_Model/Neural_Language_Model/Saved_Models/nn-model-tokenized.pth')
    ngramModelPath = os.path.join(
        dirname, '../Language_Model/Ngram_Model/my_classifier.pickle')

    insertionPath = os.path.join(
        dirname, '../error_model/Probability sets/insertion_probabilities.json')
    deletionPath = os.path.join(
        dirname, '../error_model/Probability sets/deletion_probabilities.json')
    substitutionPath = os.path.join(
        dirname, '../error_model/Probability sets/substitution_probabilities.json')
    spellChecker = SpellChecker(dictionaryPath, neuralModelPath,
                              ngramModelPath, insertionPath, deletionPath, substitutionPath)
    if request.method == 'POST':
        text = request.form['text']
        suggestions = spellChecker.correctSpelling(text)
        print(suggestions)
        return render_template('index.html', option_list=suggestions)

    return render_template('index.html', option_list=[])
