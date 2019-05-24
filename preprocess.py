import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import json
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(set('for a of the and to in'.split()))

from builtins import str
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import os



def preprocessTweets(tweetdate,file,storeFolder):
    tweets_file = open(os.path.join('Temp', file), "r")
    processed = open(os.path.join(storeFolder, tweetdate), 'w',encoding='utf-8')


    for tweet in tweets_file:
        try:
            tweet = json.loads(tweet)
            # print(datetime.(tweet['created_at']).date)
            if 'text' in tweet:

                line = tweet['text']

                # Remove @xxxx and #xxxxx
                content = [str(word.lower()) for word in line.split() if
                           word.find('@') == -1 and word.find('#') == -1 and word.find('http') == -1]

                # join words list to one string
                content = ' '.join(content)

                # remove symbols
                content = re.sub(r'[^\w]', ' ', content)

                # remove stop words
                content = [word for word in content.split() if
                           word not in stopwords.words('english') and len(word) > 3 and not any(
                               c.isdigit() for c in word)]

                # join words list to one string
                content = ' '.join(content)


                # Stemming and lemmatization
                lmtzr = WordNetLemmatizer()

                content = lmtzr.lemmatize(content)

                # Filter only nouns and adjectives
                tokenized = nltk.word_tokenize(content)
                classified = nltk.pos_tag(tokenized)

                content = [word for (word, clas) in classified if
                           clas == 'NN' or clas == 'NNS' or clas == 'NNP' or clas == 'NNPS' or clas == 'JJ' or clas == 'JJR' or clas == 'JJS']



                # join words list to one string
                content = ' '.join(content)

                if len(content) > 0:
                    # tweets.append([line[0], content, line[2]])
                    # total_tweets += 1



                    processed.write(content)
                    processed.write('\n')

        except:
            continue

    processed.close()
    tweets_file.close()
    path=os.path.join('Temp', file)
    try:
        if os.path.isfile(path):
            os.unlink(path)

    except Exception as e:
        print(e)
