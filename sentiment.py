import os

import nltk
import random
import pickle
from nltk.corpus import stopwords

short_pos = open("positive.txt", "r").read()
short_neg = open("negative.txt", "r").read()

all_words = []
documents = []
allowed_word_types = ["J"]  # adjectives only

if os.path.isfile("pickled_algos/documents.pickle"):
    print('pickled docs exists')
    save_docs = open('pickled_algos/documents.pickle', 'rb')
    documents = pickle.load(save_docs)
    save_docs.close()
else:
    print("loading pickled docs")
    # pre-processing of the text
    for p in short_pos.split('\n'):
        documents.append((p, 'pos'))
        words = nltk.word_tokenize(p)
        pos = nltk.pos_tag(words)

        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    for p in short_neg.split('\n'):
        documents.append((p, "neg"))
        words = nltk.word_tokenize(p)
        pos = nltk.pos_tag(words)
        print(pos)

        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:5662]
    print(word_features[:5])

    print('create documents')
    save_docs = open('pickled_algos/documents.pickle', 'wb')
    pickle.dump(documents, save_docs)
    save_docs.close()


# features extractor
def find_features(tweet):
    words = nltk.word_tokenize(tweet)

    filtered_words = [word for word in words if word not in stopwords.words('english')]

    features = {}
    for w in word_features:
        features[w] = (w in filtered_words)
    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)
testing_set = featuresets[5000:]
training_set = featuresets[:5662]

if os.path.isfile("pickled_algos/nltk-naive.pickle"):
        print('File exists')
        save_classifier = open('pickled_algos/nltk-naive.pickle', 'rb')
        classifier = pickle.load(save_classifier)
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
        save_classifier.close()
else:
        print('File does not exist. Generating file...')
        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
        classifier.show_most_informative_features(15)
        # create a pickle file
        save_classifier = open('pickled_algos/nltk-naive.pickle', 'wb')
        pickle.dump(classifier, save_classifier)
        save_classifier.close()


def sentiment(text):
    feats = find_features(text)
    return classifier.classify(feats)
