import pickle
# coding: utf-8

classifier = pickle.load(open('/home/felipexw/nltk_data/classifiers/gplay_manualmente_NaiveBayes.pickle'))

words = ['desde', 'sempre', 'horrario', '!']

feats = dict([(word, True) for word in words])

print classifier.classify(feats)   