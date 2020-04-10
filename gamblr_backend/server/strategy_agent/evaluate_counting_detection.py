import numpy as np
import random
from operator import add
from evaluate_strategy import gen_blackjack_counting_data
from logistic_regression_classifier import *


# Generate artificial data
#noise = np.random.normal(0,0.05,1000)
negative_train = gen_blackjack_counting_data(n_hands=10000, bet=1, method="tabular", counting=False)
negative_test = gen_blackjack_counting_data(n_hands=1000, bet=1, method="tabular", counting=False)

#noise = np.random.normal(0,0.05,1000)
positive_train = gen_blackjack_counting_data(n_hands=10000, bet=1, method="tabular", counting=True)
positive_test = gen_blackjack_counting_data(n_hands=1000, bet=1, method="tabular", counting=True)

data_train = negative_train + positive_train
data_test = negative_test + positive_test

labels_train = [0]*10000 + [1]*10000
labels_test = [0]*1000 + [1]*1000

train_dataset = list(zip(data_train, labels_train))
random.shuffle(train_dataset)
test_dataset = list(zip(data_test, labels_test))
random.shuffle(test_dataset)

data_train, labels_train = zip(*train_dataset)
data_test, labels_test = zip(*test_dataset)

data_train = np.transpose(np.array(data_train))
labels_train = np.array(labels_train)

data_test = np.transpose(np.array(data_test))
labels_test = np.array(labels_test)

print(model(data_train, labels_train, data_test, labels_test, num_iterations=20000, learning_rate=0.001))