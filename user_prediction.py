import numpy as np
import pandas as pd

header = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=header)

item_count = df.item_id.unique().shape[0]
user_count = df.user_id.unique().shape[0]

print 'Total users count = ' + str(user_count)
print 'Total movies count = ' + str(item_count)  

from sklearn import cross_validation as cv
train_data, test_data = cv.train_test_split(df, test_size=0.25)


train_mat = np.zeros((user_count, item_count))
for each in train_data:
                train_mat[each[0]-1, each[1]-1] = each[2]

test_mat = np.zeros((user_count, item_count))

for each in test_data:
                test_mat[each[0]-1, each[1]-1] = each[2]

from sklearn.metrics.pairwise import pairwise_distances
similarity_in_users = pairwise_distances(train_mat, metric='cosine')

def user_compute(ratings, similarity):
                        mean_user_rating = ratings.mean(axis=1)
                        ratings_diff = (ratings - mean_user_rating[:, np.newaxis]) 
                        user_pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T   
                        return user_pred

user_prediction = user_compute(train_mat, similarity_in_users)
