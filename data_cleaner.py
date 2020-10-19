import pandas as pd
from sqlalchemy import create_engine
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer, WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import matplotlib.pyplot as plt
from wordcloud import WordCloud
nltk.download('wordnet')
engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

# get reviews from the database
reviews = None
connection = engine.raw_connection()
columns = []
cursor = connection.cursor()
# call stored procedure
cursor.callproc("GetAll")
for result in cursor.stored_results():
    # get columns 
    columns = [column[0] for column in result.description]
    print(columns)
    reviews = pd.DataFrame(result.fetchall())
    reviews.columns = columns

cursor.close()
connection.commit()
connection.close()


reviews = reviews[reviews.review.str.count(' ') > 10] # only reviews with more than 10 words
reviews.review = reviews.review.str.lower() # convert to lowercase
reviews.review = reviews.review.str.replace('\d+','') # remove numbers
reviews.review = reviews.review.str.replace('[^\w\s]',' ') # remove punctuation
# remove stopwords and stem words 
# stop = set(stopwords.words('english'))
# snow = SnowballStemmer('english')
# reviews.review = reviews.review.apply(lambda x: [snow.stem(word) for word in x.split() if not word in stop])

# remove stopwords and lemmetize words
stop = set(stopwords.words('english'))
wordnet_lemmatizer  = WordNetLemmatizer()
reviews.review = reviews.review.apply(lambda x: [wordnet_lemmatizer.lemmatize(word) for word in x.split() if not word in stop])


print(len(reviews[reviews.label == 'positive']))
print(len(reviews[reviews.label == 'negative']))

cleaned_text = reviews.review

print(cleaned_text[1])
def do_nothing(tokens):
    return tokens


count_vect = CountVectorizer(max_features=5000, lowercase=False, tokenizer=do_nothing)
bow_data = count_vect.fit_transform(cleaned_text)
print(bow_data[1])

# try out bi grams
final_B_X = cleaned_text
count_vect = CountVectorizer(ngram_range=(1,2), lowercase=False, tokenizer=do_nothing)
Bigram_data = count_vect.fit_transform(final_B_X)
print(Bigram_data[1])

# try out TFIDF
final_tf = cleaned_text
tf_idf = TfidfVectorizer(max_features=5000, lowercase=False, tokenizer=do_nothing)
tf_data = tf_idf.fit_transform(final_tf)
print(tf_data[1])

pos_sentences = []
for row in reviews[reviews.label == 'positive'].review:
    single_row = ''
    for word in row:
       single_row = single_row + ' ' + word
    pos_sentences.append(single_row)

neg_sentences = []
for row in reviews[reviews.label == 'negative'].review:
    single_row = ''
    for word in row:
       single_row = single_row + ' ' + word
    neg_sentences.append(single_row)

wordcloud = WordCloud(width = 1000, height = 500, collocations = False).generate((" ").join(pos_sentences))
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)

wordcloud = WordCloud(width = 1000, height = 500, collocations = False).generate((" ").join(neg_sentences))
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)