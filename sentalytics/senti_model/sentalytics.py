import time
import pandas as pd
import numpy as np
import os
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


class SentalyticsClassifier:
    """
    For absolute paths to the csv files
    Using the "sentalytics/senti_model" prefix due to namespace issues
    """
    path = os.path.abspath("sentalytics/senti_model/dataset/labelled_tweets.csv")
    amazon_positive_path = os.path.abspath("sentalytics/senti_model/dataset/amazon_positive.csv")
    svm_pickle_path = os.path.abspath("sentalytics/senti_model/pickle/clf_svm.pkl")
    log_reg_pickle = os.path.abspath("sentalytics/senti_model/pickle/clf_log_reg.pkl")

    tweet = pd.read_csv(path, usecols=['text', 'polarity'])
    # https://archive.ics.uci.edu/ml/datasets/Sentiment+Labelled+Sentences
    positive_amazon = pd.read_csv(amazon_positive_path, usecols=['text', 'polarity'])
    positive_amazon = positive_amazon.dropna(axis=1, how="any")

    # Remove rows will nan values
    tweet = tweet.dropna()

    """
    preprocessing (replace user handles (@Jumia) to be empty)
    """
    pattern = "(@[A-Za-z0-9]+)|(http|https|ftp)://[a-zA-Z0-9./]+|#(\w+)"
    tweet['text'] = tweet.text.str.replace(pattern, '')

    # Due to the limited number of positive tweets,
    # I appended some positive tweets from Amazon Dataset
    # Without duplicated index
    tweet = tweet.append(positive_amazon).drop_duplicates().reset_index(drop=True)

    # Random shuffling
    tweet = tweet.reindex(np.random.permutation(tweet.index))

    # convert label to a numerical count by creating a new column
    tweet['polarity_num'] = tweet.polarity.map({'negative': 0, 'positive': 1, 'neutral': 2})

    # Define X matrix as features and y as vectors
    X = tweet.text
    y = tweet.polarity_num

    # splitting into train test sets in same format
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)

    def __init__(self):
        print("Initializing")

    def classifier_report(self, classifier, time_train, time_predict, predicted):
        print("Results for " + classifier + "\n")
        print("Training time: %fs; Prediction time: %fs" % (time_train, time_predict))
        print(classification_report(self.y_test, predicted))
        score = metrics.accuracy_score(self.y_test, predicted)
        print("Accuracy:   %0.3f" % score)

    def svm_classifer(self):
        clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                            ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42))])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists(self.svm_pickle_path)
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            clf_svm = joblib.load(self.svm_pickle_path)
        else:
            clf_svm = clf_svm.fit(self.X_train, self.y_train)
            # Create a pickle
            print("Creating pickle file ... \n")
            joblib.dump(clf_svm, self.svm_pickle_path)
        t1 = time.time()
        prediction_svm = clf_svm.predict(self.X_test)
        t2 = time.time()
        time_svm_train = t1 - t0
        time_svm_predict = t2 - t1
        self.classifier_report("SGDClassifier", time_svm_train, time_svm_predict, prediction_svm)
        return clf_svm, prediction_svm

    def log_reg_classifer(self):
        clf_log_reg = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LogisticRegression())])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists(self.log_reg_pickle)
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            clf_log_reg = joblib.load(self.log_reg_pickle)
        else:
            clf_log_reg = clf_log_reg.fit(self.X_train, self.y_train)
            # Create a pickle
            print("Creating pickle file ... \n")
            joblib.dump(clf_log_reg, self.log_reg_pickle)
        t1 = time.time()
        prediction_log_reg = clf_log_reg.predict(self.X_test)
        t2 = time.time()
        time_log_reg_train = t1 - t0
        time_log_reg_predict = t2 - t1
        self.classifier_report("Logistic Regression:", time_log_reg_train, time_log_reg_predict, prediction_log_reg)
        return clf_log_reg, prediction_log_reg

    def classify_text(self, text):
        clf = self.log_reg_classifer()
        result = clf[0].predict([text])
        return result
