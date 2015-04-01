#coding: utf-8
import pickle
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
def classify(text):
    classifier = pickle.load(open('/home/felipexw/nltk_data/classifiers/gplay_manualmente_NaiveBayes.pickle'))
    words = word_tokenize(text)
    print words
    feats = dict([(word, True) for word in words])

    return classifier.prob_classify(classifier,feats)

print classify('Felipe é um cara mau.')
   