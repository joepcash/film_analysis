import pandas as pd

# Import data
countries_db = pd.read_csv('country_codes.csv')
countries_db['code'] = countries_db['code'].str.upper()
print("countries imported")
ratings_db = pd.read_csv('ratings/title.ratings.tsv.gz', sep = '\t')
print("ratings imported")
principals_db = pd.read_csv('principals/title.principals.tsv.gz', sep = '\t')
#principals_db = principals_db[(principals_db['category'] == 'actor') | (principals_db['category'] == 'actress')]
principals_db = principals_db[principals_db['category'] == 'director']
print("principals imported")
names_db = pd.read_csv('names/name.basics.tsv.gz', sep = '\t')
print("names imported")

prin_rate = pd.merge(principals_db[['tconst','nconst']], ratings_db, on='tconst', how='left')
# Remove movies with less than x ratings
prin_rate = prin_rate[prin_rate['numVotes'] > 1000]

# Average by actor
average_by_actor = prin_rate[['nconst','averageRating', 'tconst']].groupby('nconst')\
    .agg({'tconst':'size', 'averageRating':'mean'})\
    .rename(columns = {'tconst':'count', 'averageRating':'mean_rat'})\
    .reset_index()
# Remove actors with less than 20 titles
# average_by_actor = average_by_actor[average_by_actor['count'] > 20]
# Get actor names
actor_avg = pd.merge(names_db[['nconst','primaryName']], average_by_actor, on='nconst', how='inner')

print(actor_avg[['primaryName','count','mean_rat']].sort_values(by='mean_rat',ascending=False).head(100))
actor_avg[['primaryName','count','mean_rat']].sort_values(by='mean_rat',ascending=False).to_csv(r'actor_ratings.csv', index=False)

