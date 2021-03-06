# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 14:53:14 2022

@author: Jason Harris
Individual Project 5
This code is using decision trees and Gini to create a Classification And 
Regresion Tree algorithm, and indentifying test data used in the algorithm to 
illustrate the output of the prediction. I have used the following websites 
to create this code:
https://towardsdatascience.com/decision-tree-in-machine-learning-e380942a4c96
https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/
https://www.kaggle.com/ritesaluja/bank-note-authentication-uci-data

"""
from random import seed
from random import randrange
from csv import reader

def load_csv(filename):                                         # defining the function to load the dataset instead of doing the usual direct call
    file=open(filename, "rt")
    lines=reader(file)
    dataset=list(lines)
    return dataset

def cross_validation_split(dataset, n_folds):                   # Split a dataset into k folds
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 
def accuracy_metric(actual, predicted):                         # Calculate accuracy percentage
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
def evaluate_algorithm(dataset, algorithm, n_folds, *args):     # Evaluate an algorithm using a cross validation split
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
	return scores
 
def test_split(index, value, dataset):                          # Split a dataset based on an attribute and an attribute value
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
 
def gini_index(groups, classes):                                # Calculate the Gini index for a split dataset
	# count all samples at split point
	n_instances = float(sum([len(group) for group in groups]))
	# sum weighted Gini index for each group
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		for class_val in classes:                                 # score the group based on the score for each class
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / n_instances)
	return gini
 
def get_split(dataset):                                           # Select the best split point for a dataset
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = test_split(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}
 
def to_terminal(group):                                           # Create a terminal node value
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)
 
def split(node, max_depth, min_size, depth):                      # Create child splits for a node or make terminal
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)  # splitting using terminals
		return
	if depth >= max_depth:                                        # check for max depth
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	if len(left) <= min_size:                                     # process left child
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], max_depth, min_size, depth+1)
	if len(right) <= min_size:                                    # process right child
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], max_depth, min_size, depth+1)
 
def build_tree(train, max_depth, min_size):                       # Building the decision tree
	root = get_split(train)
	split(root, max_depth, min_size, 1)
	return root

def predict(node, row):                                           # Make that tree work out a prediction
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
 
def decision_tree(train, test, max_depth, min_size):              # Classification and Regression Tree Algorithm
	tree = build_tree(train, max_depth, min_size)
	predictions = list()                                          # creating a list to store the predicitions
	for row in test:
		prediction = predict(tree, row)                           # calling the above defined prediticion
		predictions.append(prediction)                            # appending the prediticions to the list
	return(predictions)
 
seed(1)                                                           # Test CART on Bank Note dataset

filename = 'BankNote_Authentication.csv'                          # assigning the csv to a variable
dataset=load_csv(filename)                                        # importing the csv (calling the function)
n_folds = 5                                                       # evaluate algorithm
max_depth = 5
min_size = 10
scores = evaluate_algorithm(dataset, decision_tree, n_folds, max_depth, min_size)
print('Scores: %s' % scores)
print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))

