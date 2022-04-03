from distutils.log import error
from flask import Blueprint, request, render_template
import os

from Spell_Checker.CharRNN import CharRNN
from Spell_Checker.spellchecker import SpellChecker
from Spell_Checker.utils import tokenize_full

UI_BP = Blueprint('UI_BP', __name__)


@UI_BP.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@UI_BP.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@UI_BP.route('/spellcorrect/', methods=('GET', 'POST'))
def spellcorrect():
    dirname = os.path.dirname(__file__)
    dictionaryPath = os.path.join(
        dirname, '..', 'Data', 'Names', 'combined all names - dictionary - train.json')
    neuralModelPath = os.path.join(dirname, '..', 'Language_Model', 'Neural_Language_Model/Saved_Models', 'neural-model-tokenized-1024-4-2.pth')
    ngramModelPath = os.path.join(dirname, '..', 'Language_Model/Ngram_Model', 'combined - kn3.pickle')

    insertionPath = os.path.join(
        dirname, '..', 'error_model', 'Probability sets', 'insertion_probabilities.json')
    deletionPath = os.path.join(
        dirname, '..', 'error_model', 'Probability sets' , 'deletion_probabilities.json')
    substitutionPath = os.path.join(
        dirname, '..', 'error_model', 'Probability sets', 'substitution_probabilities.json')
    spellChecker = SpellChecker(dictionaryPath, neuralModelPath,
                              ngramModelPath, insertionPath, deletionPath, substitutionPath)
    if request.method == 'POST':
        text = request.form['text']
        suggestions = spellChecker.correctSpelling(text)
        errorNameAccuracy = spellChecker.evaluationModule.model.getNameAccuracyLog(tokenize_full(text))
        print(errorNameAccuracy)
        return render_template('index.html', suggestions=suggestions[:5], error_name_accuracy=errorNameAccuracy)

    return render_template('index.html', suggestions=[], error_name_accuracy=0)
