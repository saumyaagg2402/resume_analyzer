import spacy
import os

def download_spacy_model():
    try:
        nlp = spacy.load('en_core_web_lg')
    except OSError:
        os.system('python -m spacy download en_core_web_lg')