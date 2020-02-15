from encoder import Model
import pandas as pd
import numpy as np
import csv
import time
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import pickle
import warnings
import os
import random
import utils
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.externals import joblib


class train:
    def __init__(self):
        self.model = Model()

    def main(self, test_loc_folder):
        directory = os.fsencode(test_loc_folder)

        hm = os.listdir(directory)

        for test_loc in os.listdir(directory):

            test_loc = "./raw_data/" + os.fsdecode(test_loc)

            train_loc = "./data/train.csv"
            # test_loc = "./raw_data/Kyle-List of Reviews - 4841 Yonge.csv"
            # train_reviews, train_polarities, X_train = self.load_train(train_loc)
            test_reviews, test_polarities, X_test = self.load_test(test_loc)

            # log_reg = SGDClassifier(loss='log', penalty='l1', alpha=0.001)
            batch_size = 2

            # perhaps, we can use RNN on this vector than log_reg
            # train_polarities = list(train_polarities)
            test_polarities = list(test_polarities)

            # for i in np.arange(0, len(X_train), batch_size):
            #     current_X_train = X_train[i:i+batch_size]
            #     current_y_train = train_polarities[i:i+batch_size]
            #     log_reg.partial_fit(current_X_train, current_y_train, classes=[0,1])

            filename = './SGD_model.joblib.pkl'
            # _ = joblib.dump(log_reg, filename, compress=9)

            # for loading
            log_reg = joblib.load(filename)

            logreg_predictions = self.get_prediction(log_reg, X_test, test_polarities)

            pos_comp, neg_comp = self.get_sentiment_composition(logreg_predictions)

            print('current file:', test_loc)
            print('\n')

        print('done')

    def get_sentiment_composition(self, pred):
        
        # np array
        neg = (pred == 1).sum()
        pos = (pred == 0).sum()

        neg_comp = round(neg/len(pred)*100, 1)
        pos_comp = round(pos/len(pred)*100, 1)

        print("neg_comp:", neg_comp)
        print("pos_comp:", pos_comp)

        return pos_comp, neg_comp

    def get_prediction(self, log_reg, X_test, test_polarities):
        
        logreg_predictions = log_reg.predict(X_test)

        print(accuracy_score(test_polarities, logreg_predictions))

        return logreg_predictions

    def load_train(self, train_loc):
        train_reviews = []
        train_polarities = []
        with open(train_loc, 'r') as f:
            reviews_with_polarity = list(csv.reader(f))
            train_reviews = map(lambda x: x[1], reviews_with_polarity)
            train_polarities = map(lambda x: 0 if int(x[0]) >= 3 else 1, reviews_with_polarity)

        if os.path.isfile('./transformed_train_reviews.p'):
            print("Found an existing pickle file - loading....")
            X_train = pickle.load(open('transformed_train_reviews.p','rb'))
        else:
            X_train = model.transform(train_reviews)
            pickle.dump(X_train, open('transformed_train_reviews.p','wb'))

        return train_reviews, train_polarities, X_train
    
    def load_test(self, test_loc):
        test_reviews = []
        test_polarities = []
        file_name = test_loc.split("/")[-1][:-4]
        with open(test_loc, 'r', encoding='cp932', errors='ignore') as f:

            # preprocessing, only take reviews that have words
            reviews_with_polarity = list(csv.reader(f))
            reviews_with_polarity = reviews_with_polarity[1:]
            reviews_with_polarity = list(filter(lambda x: len(x[1])>0, reviews_with_polarity))

            test_reviews = map(lambda x: x[1], reviews_with_polarity)
            test_polarities = map(lambda x: 0 if int(x[0]) >= 3 else 1, reviews_with_polarity)

        if os.path.isfile(f'./{file_name}.p'):
            print("Found an existing pickle file - loading....")
            X_test = pickle.load(open(f'{file_name}.p','rb'))
        else:
            X_test, _ = self.model.transform(test_reviews)
            pickle.dump(X_test, open(f'{file_name}.p','wb'))

        return test_reviews, test_polarities, X_test

t = train()
t.main(test_loc_folder = "./raw_data/")