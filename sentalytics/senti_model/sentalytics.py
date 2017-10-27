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
from sklearn.linear_model import LogisticRegression
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
    path = os.path.abspath("sentalytics/senti_model/dataset/labelled_tweets.csv")

    tweet = pd.read_csv(path, usecols=['text', 'polarity'])

    # Remove rows will nan values
    tweet = tweet.dropna()
    tweet = tweet.reindex(np.random.permutation(tweet.index))

    """
    preprocessing (replace user handles (@Jumia) to be empty)
    """
    pattern = "(@[A-Za-z0-9]+)|(http|https|ftp)://[a-zA-Z0-9./]+|#(\w+)"
    tweet['text'] = tweet.text.str.replace(pattern, '')

    # convert label to a numerical count by creating a new column
    tweet['polarity_num'] = tweet.polarity.map({'negative': 0, 'positive': 1, 'neutral': 2})

    # Define X matrix as features and y as vectors
    X = tweet.text
    y = tweet.polarity_num

    # splitting into train test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    def __init__(self):
        print("Initializing")

    def classifier_report(self, classifier, time_train, time_predict, predicted):
        print("Results for " + classifier + "\n")
        print("Training time: %fs; Prediction time: %fs" % (time_train, time_predict))
        print(classification_report(self.y_test, predicted))
        score = metrics.accuracy_score(self.y_test, predicted)
        print("Accuracy:   %0.3f" % score)

    def nb_classifier(self):
        clf_nb = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
        t0 = time.time()
        pickle = os.path.exists('pickle/clf_nb.pkl')
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            clf_nb = joblib.load('pickle/clf_nb.pkl')
        else:
            clf_nb = clf_nb.fit(self.X_train, self.y_train)
            # Create a pickle
            joblib.dump(clf_nb, 'pickle/clf_nb.pkl')
        t1 = time.time()
        prediction_nb = clf_nb.predict(self.X_test)
        t2 = time.time()
        time_nb_train = t1 - t0
        time_nb_predict = t2 - t1
        self.classifier_report("MultinomialNB", time_nb_train, time_nb_predict, prediction_nb)
        return clf_nb, prediction_nb

    def svm_classifer(self):
        clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42))])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists('pickle/clf_svm.pkl')
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            clf_svm = joblib.load('pickle/clf_svm.pkl')
        else:
            clf_svm = clf_svm.fit(self.X_train, self.y_train)
            # Create a pickle
            joblib.dump(clf_svm, 'pickle/clf_svm.pkl')
        t1 = time.time()
        prediction_svm = clf_svm.predict(self.X_test)
        t2 = time.time()
        time_svm_train = t1 - t0
        time_svm_predict = t2 - t1
        self.classifier_report("SGDClassifier", time_svm_train, time_svm_predict, prediction_svm)
        return clf_svm, prediction_svm

    def log_reg_classifier(self):
        clf_reg = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LogisticRegression())])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists('pickle/clf_reg.pkl')
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            clf_reg = joblib.load('pickle/clf_reg.pkl')
        else:
            clf_svm = clf_reg.fit(self.X_train, self.y_train)
            # Create a pickle
            joblib.dump(clf_svm, 'pickle/clf_reg.pkl')
        t1 = time.time()
        prediction_reg = clf_reg.predict(self.X_test)
        t2 = time.time()
        time_reg_train = t1 - t0
        time_reg_predict = t2 - t1
        self.classifier_report("LogisticRegression", time_reg_train, time_reg_predict, prediction_reg)
        return clf_reg, prediction_reg

    def classify_text(self, text):
        clf = self.svm_classifer()
        result = clf[0].predict([text])
        return result

    # def vote_classifier(self):
    #     clf_svm = self.svm_classifer()
    #     clf_reg = self.log_reg_classifier()
    #     clf_nb = self.nb_classifier()
    #
    #     # scores
    #     score_svm = {clf_svm: metrics.accuracy_score(self.y_test, clf_svm[1])}
    #     score_reg = {clf_reg: metrics.accuracy_score(self.y_test, clf_reg[1])}
    #     score_nb = {clf_nb: metrics.accuracy_score(self.y_test, clf_nb[1])}
    #
    #     return max(score_nb, score_reg, score_svm)
