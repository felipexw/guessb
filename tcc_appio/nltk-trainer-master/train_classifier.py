#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, collections, functools, itertools, math, operator, os.path, re, string, sys
import nltk.data
import nltk_trainer.classification.args
from nltk.classify import DecisionTreeClassifier, MaxentClassifier, NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.stem import *
from nltk.corpus import stopwords
from nltk.corpus.reader import CategorizedPlaintextCorpusReader, CategorizedTaggedCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.metrics import BigramAssocMeasures, f_measure, masi_distance, precision, recall
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.util import ngrams
from spelling_replacer import *
from nltk_trainer import dump_object, import_attr, iteritems, load_corpus_reader
from nltk_trainer.classification import corpus, scoring
from nltk_trainer.classification.featx import (bag_of_words, bag_of_words_in_set,
	word_counts, train_test_feats, word_counts_in_set)
from nltk_trainer.classification.multi import MultiBinaryClassifier
from enchant.checker import SpellChecker

########################################
## command options & argument parsing ##
########################################
parser = argparse.ArgumentParser(description='Train a NLTK Classifier')

parser.add_argument('corpus', help='corpus name/path relative to an nltk_data directory')
parser.add_argument('--filename', help='''filename/path for where to store the
	pickled classifier, the default is {corpus}_{algorithm}.pickle in
	~/nltk_data/classifiers''')
parser.add_argument('--no-pickle', action='store_true', default=False,
	help="don't pickle and save the classifier")
parser.add_argument('--classifier', '--algorithm', default=['NaiveBayes'], nargs='+',
	choices=nltk_trainer.classification.args.classifier_choices,
	help='''Classifier algorithm to use, defaults to %(default)s. Maxent uses the
	default Maxent training algorithm, either CG or iis.''')
parser.add_argument('--trace', default=1, type=int,
	help='How much trace output you want, defaults to 1. 0 is no trace output.')
parser.add_argument('--show-most-informative', default=0, type=int,
	help='number of most informative features to show, works for all algorithms except DecisionTree')

corpus_group = parser.add_argument_group('Training Corpus')
corpus_group.add_argument('--reader',
	default='nltk.corpus.reader.CategorizedPlaintextCorpusReader',
	help='Full module path to a corpus reader class, such as %(default)s')
corpus_group.add_argument('--cat_pattern', default='(.+)/.+',
	help='''A regular expression pattern to identify categories based on file paths.
	If cat_file is also given, this pattern is used to identify corpus file ids.
	The default is '(.+)/+', which uses sub-directories as categories.''')
corpus_group.add_argument('--cat_file',
	help='relative path to a file containing category listings')
corpus_group.add_argument('--delimiter', default=' ',
	help='category delimiter for category file, defaults to space')
corpus_group.add_argument('--instances', default='files',
	choices=('sents', 'paras', 'files'),
	help='''the group of words that represents a single training instance,
	the default is to use entire files''')
corpus_group.add_argument('--fraction', default=1.0, type=float,
	help='''The fraction of the corpus to use for training a binary or
	multi-class classifier, the rest will be used for evaulation.
	The default is to use the entire corpus, and to test the classifier
	against the same training data. Any number < 1 will test against
	the remaining fraction.''')
corpus_group.add_argument('--train-prefix', default=None,
	help='optional training fileid prefix for multi classifiers')
corpus_group.add_argument('--test-prefix', default=None,
	help='optional testing fileid prefix for multi classifiers')
corpus_group.add_argument('--word-tokenizer', default='', help='Word Tokenizer class path')
corpus_group.add_argument('--sent-tokenizer', default='', help='Sent Tokenizer data.pickle path')
corpus_group.add_argument('--para-block-reader', default='', help='Block reader function path')
corpus_group.add_argument('--labels', default=[],
	help='''If given a list of labels, default categories by corpus are omitted''')

classifier_group = parser.add_argument_group('Classifier Type',
	'''A binary classifier has only 2 labels, and is the default classifier type.
	A multi-class classifier chooses one of many possible labels.
	A multi-binary classifier choose zero or more labels by combining multiple
	binary classifiers, 1 for each label.''')
classifier_group.add_argument('--binary', action='store_true', default=False,
	help='train a binary classifier, or a multi-binary classifier if --multi is also given')
classifier_group.add_argument('--multi', action='store_true', default=False,
	help='train a multi-class classifier, or a multi-binary classifier if --binary is also given')

feat_group = parser.add_argument_group('Feature Extraction',
	'The default is to lowercase every word, strip punctuation, and use stopwords')
feat_group.add_argument('--ngrams', nargs='+', type=int,
	help='use n-grams as features.')
feat_group.add_argument('--stemmer', default='', 
					choices=nltk_trainer.classification.args.stemmers_choices,					
					help='stem and lematize (normalize) each word in the corpora before the training. Aditional'+
					' information can be found at: http://www.nltk.org/api/nltk.stem.html')
feat_group.add_argument('--spelling-replacer', action='store_true', default=False,
					help='replace repeating characters in a given word based on Enchant dictionary')
feat_group.add_argument('--no-lowercase', action='store_true', default=False,
	help="don't lowercase every word")
feat_group.add_argument('--filter-stopwords', default='no',
	choices=['no']+stopwords.fileids(),
	help='language stopwords to filter, defaults to "no" to keep stopwords')
feat_group.add_argument('--punctuation', action='store_true', default=False,
	help="don't strip punctuation")
feat_group.add_argument('--value-type', default='bool', choices=('bool', 'int', 'float'),
	help='''Data type of values in featuresets. The default is bool, which ignores word counts.
	Use int to get word and/or ngram counts.''')

score_group = parser.add_argument_group('Feature Scoring',
	'The default is no scoring, all words are included as features')
score_group.add_argument('--score_fn', default='chi_sq',
	choices=[f for f in dir(BigramAssocMeasures) if not f.startswith('_')],
	help='scoring function for information gain and bigram collocations, defaults to chi_sq')
score_group.add_argument('--min_score', default=0, type=int,
	help='minimum score for a word to be included, default is 0 to include all words')
score_group.add_argument('--max_feats', default=0, type=int,
	help='maximum number of words to include, ordered by highest score, defaults is 0 to include all words')

eval_group = parser.add_argument_group('Classifier Evaluation',
	'''The default is to test the classifier against the unused fraction of the
	corpus, or against the entire corpus if the whole corpus is used for training.''')
eval_group.add_argument('--no-eval', action='store_true', default=False,
	help="don't do any evaluation")
eval_group.add_argument('--no-accuracy', action='store_true', default=False,
	help="don't evaluate accuracy")
eval_group.add_argument('--no-precision', action='store_true', default=False,
	help="don't evaluate precision")
eval_group.add_argument('--no-recall', action='store_true', default=False,
	help="don't evaluate recall")
eval_group.add_argument('--no-fmeasure', action='store_true', default=False,
	help="don't evaluate f-measure")
eval_group.add_argument('--no-masi-distance', action='store_true', default=False,
	help="don't evaluate masi distance (only applies to a multi binary classifier)")
eval_group.add_argument('--cross-fold', type=int, default=0,
	help='''If given a number greater than 2, will do cross fold validation
	instead of normal training and testing. This option implies --no-pickle,
	is useless with --trace 0 and/or --no-eval, and currently does not work
	with --multi --binary.
	''')	

nltk_trainer.classification.args.add_maxent_args(parser)
nltk_trainer.classification.args.add_decision_tree_args(parser)
nltk_trainer.classification.args.add_sklearn_args(parser)

args = parser.parse_args()

###################
## corpus reader ##
###################

reader_args = []
reader_kwargs = {}

if args.cat_file:	
	reader_kwargs['cat_file'] = args.cfat_file
	
	if args.delimiter and args.delimiter != ' ':
		reader_kwargs['delimiter'] = args.delimiter
	
	if args.cat_pattern:
		reader_args.append(args.cat_pattern)
	else:
		reader_args.append('.+/.+')
elif args.cat_pattern:
	reader_args.append(args.cat_pattern)
	reader_kwargs['cat_pattern'] = re.compile(args.cat_pattern)

if args.word_tokenizer:
	reader_kwargs['word_tokenizer'] = import_attr(args.word_tokenizer)()

if args.sent_tokenizer:
	reader_kwargs['sent_tokenizer'] = nltk.data.LazyLoader(args.sent_tokenizer)

if args.para_block_reader:
	reader_kwargs['para_block_reader'] = import_attr(args.para_block_reader)

if args.trace:
	print('loading %s' % args.corpus)

categorized_corpus = load_corpus_reader(args.corpus, args.reader,
	*reader_args, **reader_kwargs)

if not hasattr(categorized_corpus, 'categories'):
	raise ValueError('%s is does not have categories for classification')

if len(args.labels) > 0:
	labels = args.labels.split(",")
else:
	labels = categorized_corpus.categories()
nlabels = len(labels)

if args.trace:
	print('%d labels: %s' % (nlabels, labels))

if not nlabels:
	raise ValueError('corpus does not have any categories')
elif nlabels == 1:
	raise ValueError('corpus must have more than 1 category')
elif nlabels == 2 and args.multi:
	raise ValueError('corpus must have more than 2 categories if --multi is specified')
elif nlabels > 2 and not args.multi:
	raise ValueError('if corpus have more than 2 categories, then --multi must be specified')

########################
## text normalization ##
########################

if args.filter_stopwords == 'no':
	stopset = set()
else:
	stopset = set(stopwords.words(args.filter_stopwords))

def norm_words(words):
	if not args.no_lowercase:
		words = (w.lower() for w in words)
	
	if not args.punctuation:
		words = (w.strip(string.punctuation) for w in words)
		words = (w for w in words if w)
	
	if stopset:
		words = (w for w in words if w.lower() not in stopset)
	
	#spelling correction (characteres reppeated)
	if args.spelling_replacer:
		spr = SpellingReplacer()
		words = (w for w in words if spr.replace(w))
	
	#stemming and lemmatization (normalization)
	if not args.stemmer == '':
		stemmer = nltk_trainer.classification.args.get_stemmer(args.stemmer)
		stemmer = stemmer()
		words = (w for w in words if stemmer.stem(w))
		
	# in case we modified words in a generator, ensure it's a list so we can add together
	if not isinstance(words, list):
		words = list(words)
	
	if args.ngrams:
		return functools.reduce(operator.add, [words if n == 1 else list(ngrams(words, n)) for n in args.ngrams])
	else:
		return words


#####################
## text extraction ##
#####################
if args.multi and args.binary:
	label_instance_function = {
		'sents': corpus.multi_category_sent_words,
		'paras': corpus.multi_category_para_words,
		'files': corpus.multi_category_file_words
	}
	
	lif = label_instance_function[args.instances]
	train_instances = lif(categorized_corpus, args.train_prefix)
	test_instances = lif(categorized_corpus, args.test_prefix)

	# if we need all the words by category for score_fn, use this method
	def category_words():
		'''
		return an iteration of tuples of category and list of all words in instances of that category.
		Used if we are scoring the words for correlation to categories for feature selection (i.e.,
		score_fn and max_feats are set)
		'''
		cat_words = defaultdict([])
		for (words, cats) in train_instances:
			if isinstance(cats, collections.Iterable):
				for cat in cats:
					cat_words[cat].extend(words)
			else:
				cat_words[cats].extend(words)
		return iteritems(cat_words)

else:
	def split_list(lis, fraction):
		'''split a list into 2 lists based on the fraction provided. Used to break the instances into 
		   train and test sets'''
		if fraction != 1.0:
			l = len(lis)
			cutoff = int(math.ceil(l * fraction))
			return lis[0:cutoff], lis[cutoff:]
		else:
			return lis, []

	label_instance_function = {
		'sents': corpus.category_sent_words,
		'paras': corpus.category_para_words,
		'files': corpus.category_file_words
	}
	
	lif = label_instance_function[args.instances]
	train_instances = {}
	test_instances = {}
	
	for label in labels:
		instances = (norm_words(i) for i in lif(categorized_corpus, label))
		instances = [i for i in instances if i]
		train_instances[label], test_instances[label] = split_list(instances, args.fraction)
		if args.trace > 1:
			info = (label, len(train_instances[label]), len(test_instances[label]))
			print('%s: %d training instances, %d testing instances' % info)
	# if we need all the words by category for score_fn, use this method
	def category_words():
		'''
		return an iteration of tuples of category and list of all words in instances of that category.
		Used if we are scoring the words for correlation to categories for feature selection (i.e.,
		score_fn and max_feats are set)
		'''
		return ((cat, (word for i in instance_list for word in i)) for cat, instance_list in iteritems(train_instances))					

##################
## word scoring ##
##################

score_fn = getattr(BigramAssocMeasures, args.score_fn)

if args.min_score or args.max_feats:
	if args.trace:
		print('calculating word scores')
	
	# flatten the list of instances to a single iteration of all the words 
	cat_words = category_words()
	ws = scoring.sorted_word_scores(scoring.sum_category_word_scores(cat_words, score_fn))
	
	if args.min_score:
		ws = [(w, s) for (w, s) in ws if s >= args.min_score]
	
	if args.max_feats:
		ws = ws[:args.max_feats]
	
	bestwords = set([w for (w, s) in ws])
	
	if args.value_type == 'bool':
		if args.trace:
			print('using bag of words from known set feature extraction')
		
		featx = lambda words: bag_of_words_in_set(words, bestwords)
	else:
		if args.trace:
			print('using word counts from known set feature extraction')
		
		featx = lambda words: word_counts_in_set(words, bestwords)
	
	if args.trace:
		print('%d words meet min_score and/or max_feats' % len(bestwords))
elif args.value_type == 'bool':
	if args.trace:
		print('using bag of words feature extraction')
	
	featx = bag_of_words
else:
	if args.trace:
		print('using word counts feature extraction')
	
	featx = word_counts

		
#########################
## extracting features ##
#########################
def extract_features(label_instances, featx):
	if isinstance(label_instances, dict):
		# for not (args.multi and args.binary)
        # e.g., li = { 'spam': [ ['hello','world',...], ... ], 'ham': [ ['lorem','ipsum'...], ... ] }
		feats = []
		for label, instances in iteritems(label_instances):
			feats.extend([(featx(i), label) for i in instances])
	else:
		# for arg.multi and args.binary
		# e.g., li = [ (['hello','world',...],label1), (['lorem','ipsum'],label2) ]
		feats = [(featx(i), label) for i, label in label_instances ]
	return feats

	
train_feats = extract_features(train_instances, featx)
test_feats = extract_features(test_instances, featx)
# if there were no instances reserved for testing, test over the whole training set
if not test_feats:
	test_feats = train_feats

if args.trace:
       print('%d training feats, %d testing feats' % (len(train_feats), len(test_feats)))

##############
## training ##
##############
trainf = nltk_trainer.classification.args.make_classifier_builder(args)
entrou = False
classifier = None

if args.cross_fold:
	if args.multi and args.binary:
		raise NotImplementedError ("cross-fold is not supported for multi-binary classifiers")
	##IMPLEMENTAR AQUI
	entrou = True
	#accuracies, precisions, recalls, f_measures, classifier = scoring.cross_fold(train_feats, trainf, accuracy, folds=args.cross_fold,
	#	trace=args.trace, metrics=not args.no_eval, informative=args.show_most_informative)
	accuracies, precisions, recalls, f_measures, classifier = scoring.k_fold_validation(train_feats, trainf, accuracy, folds=args.cross_fold,
		trace=args.trace, metrics=not args.no_eval, informative=args.show_most_informative)

if args.multi and args.binary:
	if args.trace:
		print('training multi-binary %s classifier' % args.classifier)
	classifier = MultiBinaryClassifier.train(labels, train_feats, trainf)

elif not entrou:
	classifier = trainf(train_feats)

################
## evaluation ##
################
if not args.no_eval and not args.cross_fold > 2:
	if not args.no_accuracy:
		try:
			print('accuracy: %f' % accuracy(classifier, test_feats))
		except ZeroDivisionError:
			print('accuracy: 0')

	if args.multi and args.binary and not args.no_masi_distance:
		print('average masi distance: %f' % (scoring.avg_masi_distance(classifier, test_feats)))
	
	if not args.no_precision or not args.no_recall or not args.no_fmeasure:
		if args.multi and args.binary:
			refsets, testsets = scoring.multi_ref_test_sets(classifier, test_feats)
		else:
			refsets, testsets = scoring.ref_test_sets(classifier, test_feats)
		
		for label in labels:
			ref = refsets[label]
			test = testsets[label]
			
			if not args.no_precision:
				print('%s precision: %f' % (label, precision(ref, test) or 0))
			
			if not args.no_recall:
				print('%s recall: %f' % (label, recall(ref, test) or 0))
			
			if not args.no_fmeasure:
				print('%s f-measure: %f' % (label, f_measure(ref, test) or 0))

####################################
## showing most informative words ##
####################################
if args.show_most_informative and hasattr(classifier, 'show_most_informative_features') and not (args.multi and args.binary) and not args.cross_fold:
	print('%d most informative features' % args.show_most_informative)
	classifier.show_most_informative_features(args.show_most_informative)
	
##############
## pickling ##
##############
if not args.no_pickle:
	if args.filename:
		fname = os.path.expanduser(args.filename)
	else:
		corpus_clean = os.path.split(args.corpus.rstrip('/'))[1]
		name = '%s_%s.pickle' % (corpus_clean, '_'.join(args.classifier))
		fname = os.path.join(os.path.expanduser('~/nltk_data/classifiers'), name)
	
	dump_object(classifier, fname, trace=args.trace)

