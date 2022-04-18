# Bank_Note
Bank Note Authentication Algorithm

One of the machine learning techniques is splitting the data into trees, in order to make predictions. 
Imagine the root of a tree that goes up into the trunk, and that is then split into branches and those branches are split 
into branches with each split being homogeneous, similar to a binary tree. 
I have chosen to use the Classification And Regression Tree (CART) and, carrying on with our bank fraud detection theme, 
I have applied it to the dataset “Banknote Authentication” (https://www.kaggle.com/ritesaluja/bank-note-authentication-uci-data) 
(checks for those of us raised in the United States). 
I chose to use the CART due to the fact that it is a combination of both the classification and the regression predictive models. 
This approach allows for different splitting techniques to be trialed and tested before choosing the most efficient one, and because 
why not try a combination when I have been doing singular algorithms in the last few projects. This particular tutorial that I have 
followed focuses on the classification tree functions of the CART. Using the Gini cost function, nodes are provided with a purity 
indication that helps to control the split function. Using this split method, the algorithm was able to predict and achieve an accuracy 
of 95.255% on the given dataset. The code has been properly commented to explain what is occurring at each step.
