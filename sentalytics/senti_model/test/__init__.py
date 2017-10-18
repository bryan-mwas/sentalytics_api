import time
import pandas as pd
import numpy as np
import os

import sentalytics.senti_model.preprocessing as pre

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

if __name__ == '__main__':
    # Access the csv file
    df = pd.read_csv('.\\dataset\\labelled_tweets.csv', skipinitialspace=True, usecols=['text', 'polarity'])
    df.dropna(how='any')

    # print(type(df))
    text = df['text']
    label = df['polarity']


    # Split the tweets in training and test set
    def split_data(data):
        # shuffle data
        data.reindex(np.random.permutation(data.index))

        # train, test data
        train, test = train_test_split(data, test_size=0.3)

        train.to_csv(".\\dataset\\train_data.csv")
        test.to_csv(".\\dataset\\test_data.csv")


    #     split_data(df)

    train = pd.read_csv(".\\dataset\\train_data.csv", skipinitialspace=True, encoding='latin1')
    train_text = train['text']
    train_label = train['polarity']

    test = pd.read_csv(".\\dataset\\test_data.csv", skipinitialspace=True, encoding='latin1')
    test_text = test['text']
    test_label = test['polarity']


    # Remove handles and hashtags
    # TODO: Review removal of hyperlinks
    def normalized_data(dataset):
        cleaned_text = []
        for index, item in enumerate(dataset.text):
            if isinstance(item, str):
                cleaned_text.append(pre.process_text(item))
        return cleaned_text


    def polarity(dataset):
        polarity = []
        for index, item in enumerate(dataset.polarity):
            if isinstance(item, str):
                polarity.append(pre.process_text(item))
        return polarity


    def classifier_report(classifier, time_train, time_predict, predicted):
        print("Results for " + classifier + "\n")
        print("Training time: %fs; Prediction time: %fs" % (time_train, time_predict))
        print(classification_report(polarity(test), predicted))
        score = metrics.accuracy_score(polarity(test), predicted)
        print("Accuracy:   %0.3f" % score)


    def nb_classifier():
        text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', BernoulliNB())])
        t0 = time.time()
        text_clf = text_clf.fit(normalized_data(train), polarity(train))
        t1 = time.time()
        prediction_nb = text_clf.predict(normalized_data(test))
        t2 = time.time()
        time_nb_train = t1 - t0
        time_nb_predict = t2 - t1
        classifier_report("MultinomialNB", time_nb_train, time_nb_predict, prediction_nb)


    def svm_classifer():
        text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), (
        'clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, max_iter=5, random_state=42)), ])
        t0 = time.time()
        # Check if a pickled file exists
        pickle = os.path.exists('text_clf_svm.pkl')
        if pickle:
            print("Pickle file exists. Loading pickle ... \n")
            text_clf_svm = joblib.load('text_clf_svm.pkl')
        else:
            text_clf_svm = text_clf_svm.fit(normalized_data(train), polarity(train))
            # Create a pickle
            joblib.dump(text_clf_svm, 'text_clf_svm.pkl')
        t1 = time.time()
        prediction_svm = text_clf_svm.predict(normalized_data(test))
        t2 = time.time()
        time_svm_train = t1 - t0
        time_svm_predict = t2 - t1
        classifier_report("SGDClassifier", time_svm_train, time_svm_predict, prediction_svm)
        return text_clf_svm