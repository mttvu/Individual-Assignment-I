import pandas as pd
from sqlalchemy import create_engine

reviews = []

reviews.append(["""The service was terrible. 
When we arrived at the hotel we had to wait an hour before we could get to our room. Then when we 
finally got there, it was super messy. I also found bedbugs in our bed. Really gross.""",'negative'])

reviews.append(["""The service was great. Our room was really clean and the food was amazing. 
The staff was really friendly. I will go to this hotel again when I am here the next time. """,
'positive'])

reviews.append(["""I called for room service but no one came to my room. Terrible service. 
Also did not enjoy the food. It was very bland. Would not recommend to other people""", 'negative'])

reviews_df = pd.DataFrame(reviews, columns=['review','label'])

engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

reviews_df.to_sql(name='reviews',con=engine,if_exists='append',index=False) 