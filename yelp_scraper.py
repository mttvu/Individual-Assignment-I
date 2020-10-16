from bs4 import BeautifulSoup as bs
import requests
import logging
import pandas as pd
import re
from sqlalchemy import create_engine

start_page = 'https://www.yelp.com/biz/grand-bohemian-hotel-orlando-autograph-collection-orlando-3?start='

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

counter = 0
scraped_reviews = []

def get_links(url):
    global counter 

    response = requests.get(url, headers=headers)
    counter += 20
    print(counter)
    if(response.status_code == 200):
        soup = bs(response.text, 'html.parser')
        parse_review_page(soup)
        next_url = soup.select('a.next-link')
        if next_url:
            next_url = start_page + str(counter)
            get_links(next_url)

    


def parse_review_page(soup):
    global scraped_reviews
    for review in soup.findAll('li', class_='lemon--li__373c0__1r9wz margin-b3__373c0__q1DuY padding-b3__373c0__342DA border--bottom__373c0__3qNtD border-color--default__373c0__3-ifU'):
        
        review_text = review.find('span', {'class': 'lemon--span__373c0__3997G raw__373c0__3rKqk', 'lang':'en'})
        rating = review.find('div', class_='i-stars__373c0__1T6rz')
        print(rating)
        if rating:
            if rating['aria-label']:
                rating = re.findall('\d+', rating['aria-label'])[0]
        
            if review_text:
                review_text = review_text.text
                if(int(rating) > 2):
                    scraped_reviews.append([review_text,'positive'])
                else:
                    scraped_reviews.append([review_text,'negative'])




get_links(start_page + str(counter))

reviews_df = pd.DataFrame(scraped_reviews, columns=['review','label'])

engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

reviews_df.to_sql(name='reviews',con=engine,if_exists='append',index=False) 