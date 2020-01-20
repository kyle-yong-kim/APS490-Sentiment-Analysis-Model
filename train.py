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

# model = Model()

train_loc = "./data/train.csv"
test_loc = "./data/test.csv"

train_reviews = []
train_polarities = []
with open(train_loc, 'r') as f:
    reviews_with_polarity = list(csv.reader(f))
    train_reviews = map(lambda x: x[1], reviews_with_polarity)
    train_polarities = map(lambda x: 0 if int(x[0]) >= 3 else 1, reviews_with_polarity)

test_reviews = []
test_polarities = []
with open(test_loc, 'r') as f:
    reviews_with_polarity = list(csv.reader(f))
    test_reviews = map(lambda x: x[1], reviews_with_polarity)
    test_polarities = map(lambda x: int(x[0]), reviews_with_polarity)

if os.path.isfile('./transformed_train_reviews.p'):
    print("Found an existing pickle file - loading....")
    X_train = pickle.load(open('transformed_train_reviews.p','rb'))
else:
    X_train = model.transform(train_reviews)
    pickle.dump(X_train, open('transformed_train_reviews.p','wb'))

if os.path.isfile('./transformed_test_reviews.p'):
    print("Found an existing pickle file - loading....")
    X_test = pickle.load(open('transformed_test_reviews.p','rb'))
else:
    X_test = model.transform(test_reviews)
    pickle.dump(X_test, open('transformed_test_reviews.p','wb'))

log_reg = SGDClassifier(loss='log', penalty='l1', alpha=0.001)
batch_size = 2

# perhaps, we can use RNN on this vector than log_reg
train_polarities = list(train_polarities)
test_polarities = list(test_polarities)
for i in np.arange(0, len(X_train), batch_size):
    current_X_train = X_train[i:i+batch_size]
    current_y_train = train_polarities[i:i+batch_size]
    log_reg.partial_fit(current_X_train, current_y_train, classes=[0,1])

logreg_predictions = log_reg.predict(X_test)
print(accuracy_score(test_polarities, logreg_predictions))