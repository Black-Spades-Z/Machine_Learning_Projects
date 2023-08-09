# Importing library

import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

# Reading csv anime

anime_df = pd.read_csv('data/anime.csv', index_col=False)
anime_1 = anime_df[['MAL_ID', 'Name', 'Score']]

# Dropping unknown labels

anime = pd.DataFrame({'MAL_ID':[1], 'Name': ['Cowboy Bebop'], 'Score': ['8.78'] })

i = 0

for x in range(1, len(anime_1)):
    if anime_1.iloc[x].Score != 'Unknown':
        i+=1
        anime.loc[i] = anime_1.iloc[x].to_list()

anime['Score'] = anime['Score'].astype('float64')

# Taking anime only with 7 + Score

temp_anime = pd.DataFrame({'MAL_ID':[1], 'Name': ['Cowboy Bebop'], 'Score': ['8.78']})
i = 0

for x in range(1, len(anime)):
    if anime.iloc[x].Score >= 7.00:
        i +=1
        temp_anime.loc[i] = anime.iloc[x]


"""
As we picked up 7 + score anime, we don't need "Score" column and temp dataframe, also we need to change MAL_ID
to anime_id as we have to connect it to another bigger dataframe with this column
"""

del anime
anime = temp_anime[['MAL_ID', 'Name']]
anime.reset_index(inplace=True, drop=True)
anime = anime.rename(columns={'MAL_ID' : 'anime_id'})

# Reading the Bigger column with rates by watchers

anime_watchers_df = pd.read_csv('data/rating_complete.csv')
anime_watchers_df = anime_watchers_df.head(200000)
anime_watchers_df.reset_index(inplace=True, drop=True)

anime_watchers = pd.DataFrame()
anime_watchers = pd.merge(anime_watchers_df, anime, on='anime_id')

# Creating a pivot table

table = pd.pivot_table(anime_watchers, values='rating', columns='Name', index='user_id')



# Creating function for finding similar anime

def get_similar_anime(anime_name, anime_score):
    similar_score = item_similarity_df[anime_name]*(anime_score - 3)
    similar_score = similar_score.sort_values(ascending=False)

    return similar_score

# Turning to testing

def standardize(row):
    new_row = (row - row.mean())/(row.max() - row.min())
    return new_row

table_std = table.apply(standardize)

# Filling NaN

table_std.fillna(0, inplace=True)

item_similarity = cosine_similarity(table_std.T)

item_similarity_df = pd.DataFrame(item_similarity, index=table.columns, columns=table.columns)

# Making list of new users preferences

for index in range(20):
    print("Please rate from 0 to 10 this anime : ")

    anime_watcher_score = int(input(anime_names + ": "))
    anime_list = anime_list.append(anime_names, anime_watcher_score)

# Starting searching

similar_anime = pd.DataFrame()

for anime, rating in anime_list:
    similar_anime = similar_anime.append(get_similar_anime(anime, rating), ignore_index=True)


similar_anime.sum().sort_values(ascending=False)




