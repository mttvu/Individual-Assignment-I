from bs4 import BeautifulSoup as bs
import requests
import logging
import pandas as pd
import re
from sqlalchemy import create_engine
import emoji

base_url = 'https://www.booking.com'

start_page = 'https://www.booking.com/reviewlist.en-gb.html?aid=304142&label=gen173bo-1DCAso3QFCFXNpcmktaGVyaXRhZ2UtYmFuZ2tva0gJWANoqQGIAQGYAQm4ARfIAQzYAQPoAQH4AQKIAgGYAgKoAgO4AoPyh_sFwAIB0gIkNzljYjk3MTYtMzQ5Zi00NmY0LWFjODMtN2RiY2E3M2JiM2Fh2AIE4AIB&sid=8a6ccf52d2f8a046cbef92a9a559ddd3&cc1=th&dist=1&pagename=siri-heritage-bangkok&type=total&rows=10&offset=0'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

counter = 0
scraped_reviews = []

def get_links(url):
    global counter 
    counter += 1
    print(counter)

    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        soup = bs(response.text, 'html.parser')
        parse_review_page(soup)
        next_url = soup.select('div.bui-pagination__next-arrow a')
        if next_url:
            next_url = base_url + next_url[0]['href']
            get_links(next_url)


def parse_review_page(soup):
    global scraped_reviews
    for review in soup.findAll('div', class_='c-review__row'):
        review_text = review.find('span', {'class': 'c-review__body', 'lang':'en'})
        if review_text:
            review_text = review_text.text
            if('lalala' in review['class']):
                scraped_reviews.append([review_text,'negative'])
            else:
                scraped_reviews.append([review_text,'positive'])


def remove_emoji(text):
    only_alphanumeric = re.sub('[^a-zA-Z0-9]', ' ', text)
    return only_alphanumeric

get_links(start_page)

reviews_df = pd.DataFrame(scraped_reviews, columns=['review','label'])

no_comments = 'There are no comments available for this review'

reviews_df['review'] = reviews_df['review'].apply(remove_emoji)
reviews_df = reviews_df[~pd.isna(reviews_df.review)]
reviews_df = reviews_df[(reviews_df.review != 'none') & (reviews_df.review != 'Nothing') & (reviews_df.review != 'None') & (~reviews_df.review.str.contains(no_comments)) ]

reviews_df.astype(str)
reviews_df.dtypes

reviews_df['review'] = reviews_df['review'].astype(str)
reviews_df['label'] = reviews_df['label'].astype(str)

engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

reviews_df.to_sql(name='reviews',con=engine,if_exists='append',index=False) 