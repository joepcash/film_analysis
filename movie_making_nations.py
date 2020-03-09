import pandas as pd

# Import data
countries_db = pd.read_csv('country_codes.csv')
countries_db['code'] = countries_db['code'].str.upper()
print("countries imported")
ratings_db = pd.read_csv('ratings/title.ratings.tsv.gz', sep = '\t')
print("ratings imported")
akas_db = pd.read_csv('akas/title.akas.tsv.gz', sep = '\t', na_values='\\N', encoding='utf-8')
print("akas imported")
#principals_db = pd.read_csv('principals/title.principals.tsv.gz', sep = '\t')
#print("principals imported")
basics_db = pd.read_csv('basics/title.basics.tsv.gz', sep = '\t')
print("basics imported")

# Remove movies with less than x ratings
ratings_db = ratings_db[ratings_db['numVotes'] > 1000]

# Join based on original title (title from the production country)
# to only return results from the country of production
original_titles = pd.merge(akas_db[['titleId', 'title','region']], basics_db[['originalTitle']], left_on='title', right_on='originalTitle', how = 'inner')
# Join to ratings db
named_ratings = pd.merge(original_titles[['titleId', 'title','region']], ratings_db, left_on='titleId', right_on='tconst', how = 'inner')
# Average by country
average_by_region = named_ratings[['region','averageRating', 'titleId']].groupby('region')\
    .agg({'titleId':'size', 'averageRating':'mean'})\
    .rename(columns = {'titleId':'count', 'averageRating':'mean_rat'})\
    .reset_index()
# Remove countries with less than 20 titles
average_by_region = average_by_region[average_by_region['count'] > 20]
# Get country name from country code
country_avg = pd.merge(countries_db, average_by_region, left_on='code', right_on='region', how='inner')


print(country_avg[['country','count','mean_rat']].sort_values(by='mean_rat',ascending=False).head(100))
country_avg[['country','count','mean_rat']].sort_values(by='mean_rat',ascending=False).to_csv(r'movie_making_nations.csv', index=False)