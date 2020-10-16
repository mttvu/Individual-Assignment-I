import pandas as pd
from sqlalchemy import create_engine

kaggle_df=pd.read_csv('2142_3597_bundle_archive\Hotel_Reviews.csv', sep=',')

positive_reviews = kaggle_df[kaggle_df['Positive_Review'] != 'No Positive']['Positive_Review'].to_frame()
negative_reviews = kaggle_df[(kaggle_df['Negative_Review'] != 'No Negative') & (kaggle_df['Negative_Review'] != 'Nothing')]['Negative_Review'].to_frame() 

positive_reviews['label'] = 'positive'
negative_reviews['label'] = 'negative'

positive_reviews.columns = ['review','label']
negative_reviews.columns = ['review','label']

all_reviews = pd.concat([positive_reviews, negative_reviews])

engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

all_reviews.to_sql(name='reviews',con=engine,if_exists='replace',index=False, chunksize=10000) 