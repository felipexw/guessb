#coding: utf-8
import pickle
from nltk.tokenize import word_tokenize
from guessb.settings import BASE_DIR, CLASSIFIER_DIR


class NBClassifierLoader(object):
    def classify(self,text):
        #CAMINHO_CLASSIFICADOR =  BASE_DIR+'/tcc_appio/nltk_trainer_master/data/classifiers/gplay_manualmente_sklearn.MultinomialNB.pickle'
    
        classifier = pickle.load(open(CLASSIFIER_DIR))
        words = word_tokenize(text)
        feats = dict([(word, True) for word in words])
        return classifier.classify(feats)
