import time
import pandas as pd
import numpy as np
import os
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from sklearn import metrics


class SentalyticsClassifier:
    """
    For absolute paths to the csv files
    Using the "sentalytics/senti_model" prefix due to namespace issues
    """
    df_url = os.path.abspath("sentalytics/senti_model/dataset/labelled_tweets.csv")
    train_url = os.path.abspath("sentalytics/senti_model/dataset/train_data.csv")
    test_url = os.path.abspath("sentalytics/senti_model/dataset/test_data.csv")

    df = pd.read_csv(df_url, skipinitialspace=True, usecols=['text', 'polarity'])
    df.dropna(how='any')
    train = pd.read_csv(train_url, skipinitialspace=True, encoding='latin1')
    test = pd.read_csv(test_url, skipinitialspace=True, encoding='latin1')

    def __init__(self):
        print("Initializing")

    def split_data(self, data):
        # shuffle data
        data.reindex(np.random.permutation(data.index))

        # train, test data
        train, test = train_test_split(data, test_size=0.3)

        train.to_csv(".\\dataset\\train_data.csv")
        test.to_csv(".\\dataset\\test_data.csv")

        # Remove handles and hashtags

    # TODO: Review removal of hyperlinks
    def normalized_data(self, dataset):
        cleaned_text = []
        for index, item in enumerate(dataset.text):
            if isinstance(item, str):
                cleaned_text.append(self.process_text(item))
        return cleaned_text

    def process_text(self, text):
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(http|https|ftp)://[a-zA-Z0-9./]+|#(\w+)", " ", text).split())
        return text.lower()

    def polarity(self, dataset):
        polarity = []
        for index, item in enumerate(dataset.polarity):
            if isinstance(item, str):
                polarity.append(self.process_text(item))
        return polarity

    def classifier_report(self, classifier, time_train, time_predict, predicted):
        print("Results for " + classifier + "\n")
        print("Training time: %fs; Prediction time: %fs" % (time_train, time_predict))
        print(classification_report(self.polarity(self.test), predicted))
        score = metrics.accuracy_score(self.polarity(self.test), predicted)
        print("Accuracy:   %0.3f" % score)

    def nb_classifier(self):
        text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', BernoulliNB())])
        t0 = time.time()
        text_clf = text_clf.fit(self, self.normalized_data(self.train), self.polarity(self.train))
        t1 = time.time()
        prediction_nb = text_clf.predict(self.normalized_data(self.test))
        t2 = time.time()
        time_nb_train = t1 - t0
        time_nb_predict = t2 - t1
        self.classifier_report("MultinomialNB", time_nb_train, time_nb_predict, prediction_nb)

    def svm_classifer(self):
        text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), (
        'clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=5, random_state=42)), ])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists('text_clf_svm.pkl')
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            text_clf_svm = joblib.load('text_clf_svm.pkl')
        else:
            text_clf_svm = text_clf_svm.fit(self.normalized_data(self.train), self.polarity(self.train))
            # Create a pickle
            joblib.dump(text_clf_svm, 'text_clf_svm.pkl')
        t1 = time.time()
        prediction_svm = text_clf_svm.predict(self.normalized_data(self.test))
        t2 = time.time()
        time_svm_train = t1 - t0
        time_svm_predict = t2 - t1
        self.classifier_report("SGDClassifier", time_svm_train, time_svm_predict, prediction_svm)
        return text_clf_svm

    def classify_svm(self, text):
        clf = self.svm_classifer()
        result = clf.predict([text])
        return result