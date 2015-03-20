import pickle

classifier = pickle.load(open('/home/felipexw/nltk_data/classifiers/movie_reviews_NaiveBayes.pickle'))

words = ["you", 'are', 'idiot ' ]
    

feats = dict([(word, True) for word in words])

print classifier.classify(feats)