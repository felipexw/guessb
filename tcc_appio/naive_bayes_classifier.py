#coding: utf-8
import pickle
from nltk.tokenize import word_tokenize
from settings import BASE_DIR


def classify(text):
    CAMINHO_CLASSIFICADOR =  BASE_DIR+'/tcc_appio/nltk-trainer-master/data/classifiers/gplay_manualmente_sklearn.MultinomialNB.pickle'
       
    classifier = pickle.load(open(CAMINHO_CLASSIFICADOR))
    words = word_tokenize(text)
    print words
    feats = dict([(word, True) for word in words])
    return classifier.classify(feats)
