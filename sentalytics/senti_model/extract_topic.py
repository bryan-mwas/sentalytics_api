from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np


class ExtractTopic:
    def __init__(self):
        print("Initializing!")

    def display_topics(self, h, w, feature_names, documents, no_top_words, no_top_documents):
        global prevalent_topics, docs
        prevalent_topics = []
        docs = []
        for topic_idx, topic in enumerate(h):
            topics = {}  # create empty dictionary
            print("Topic %d:" % topic_idx)
            print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
            major_topic = " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
            topics['major_topic'] = major_topic  # add a major_topic field
            top_doc_indices = np.argsort(w[:, topic_idx])[::-1][0:no_top_documents]
            docs = []
            for doc_index in top_doc_indices:
                print(documents[doc_index])
                docs.append(documents[doc_index])
                topics['documents'] = docs  # insert an array of document corresponding to major_topic
            prevalent_topics.append(topics)
        return prevalent_topics

    no_topics = 3
    no_top_words = 4
    no_top_documents = 4

    def nmf_extract(self, X):
        # NMF is able to use tf-idf
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(X)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()

        # Run NMF
        nmf_model = NMF(n_components=self.no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)
        nmf_W = nmf_model.transform(tfidf)
        nmf_H = nmf_model.components_
        return self.display_topics(nmf_H, nmf_W, tfidf_feature_names, X, self.no_top_words, self.no_top_documents)

    def lda_extract(self, X):
        # Run LDA
        # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
        tf = tf_vectorizer.fit_transform(X)
        tf_feature_names = tf_vectorizer.get_feature_names()

        lda_model = LatentDirichletAllocation(n_topics=self.no_topics, max_iter=5, learning_method='online',
                                              learning_offset=50.,
                                              random_state=0).fit(tf)
        lda_W = lda_model.transform(tf)
        lda_H = lda_model.components_

        return self.display_topics(lda_H, lda_W, tf_feature_names, X, self.no_top_words, self.no_top_documents)
