# Generate dat file with tweets
# @author Matias Hurtado - PUC Chile

# Import some modules for reading and getting data.
# If you don't have this modules, you must install them.


from builtins import str

from gensim import corpora, models, similarities  # to create a dictionary
import os
import csv


import tethne.model.corpus.dtmmodel as dtmmodel

# Set years, this would be the timestamps
#time_stamps = [['51', '52', '53', '54', '55'], ['56', '57', '58', '59', '0'], ['1', '2', '3', '4', '5']]






class FileMaker:
    def __init__(self,path,timestamps):
        self.path=path
        self.timestamps=timestamps


        self.dat_outfile = open(os.path.join('data', 'metadata.dat'), 'w',encoding='utf-8')
        self.tweets = list()
        self.cont=[]
        # time_stamps=setTimePeriod(self.start,self.end)




    def writeToFiles(self):
        self.dat_outfile.write('id\tdate\tcontent\n')  # write header

        # Set total_tweets list per year, starting at 0
        # total_tweets_list = [0 for year in conferences_years]
        total_tweets_list = [0 for timestamp in self.timestamps]

        # Analyze each year..

        time_stamps_count = 0

        j = 0
        for timestamp in self.timestamps:  # For each minute array
            '''
            prefix='2019-04-'
            total_tweets = 0
            preprocessed_outfile = open(os.path.join(self.path, prefix+timestamp), 'r')
            '''
            total_tweets = 0
            preprocessed_outfile = open(os.path.join(self.path, timestamp), 'r',encoding='utf-8')

            for line in preprocessed_outfile:
                total_tweets += 1
                self.dat_outfile.write(str(j) + '\t' + timestamp + '\t' + line)
                self.cont.append(line.split())

                j = j + 1
            preprocessed_outfile.close()

            # Add the total tweets to the total tweets per year list
            total_tweets_list[time_stamps_count] += total_tweets
            time_stamps_count += 1

        self.dat_outfile.close()  # Close the tweets file

        # Write seq file
        seq_outfile = open(os.path.join('data', '-seq.dat'), 'w',encoding='utf-8')
        seq_outfile.write(str(len(total_tweets_list)) + '\n')  # number of TimeStamps

        for count in total_tweets_list:
            seq_outfile.write(str(count) + '\n')  # write the total tweets per year (timestamp)

        seq_outfile.close()

        print('Done collecting tweets and writing seq')

        corpus_memory_friendly = MyCorpus(cont=self.cont)

        multFile = open(os.path.join('data', '-mult.dat'), 'w',encoding='utf-8')

        for vector in corpus_memory_friendly:  # load one vector into memory at a time
            multFile.write(str(len(vector)) + ' ')
            for (wordID, weigth) in vector:
                multFile.write(str(wordID) + ':' + str(weigth) + ' ')

            multFile.write('\n')

        multFile.close()

        print('Mult file saved')


class MyCorpus(object):
    def __init__(self, cont=None):

        self.cont = cont
        self.prepare_dictionary()


    def __iter__(self):
        for line in self.cont:
            # assume there's one document per line, tokens separated by whitespace
            yield self.dictionary.doc2bow(line)

    def prepare_dictionary(self):
        stop_list = set('for a of the and to in'.split())  # List of stop words which can also be loaded from a file.

        # Creating a dictionary using stored the text file and the Dictionary class defined by Gensim.
        self.dictionary = corpora.Dictionary(self.cont)

        # Collecting the id's of the tokens which exist in the stop-list
        stop_ids = [self.dictionary.token2id[stop_word] for stop_word in stop_list if
                    stop_word in self.dictionary.token2id]

        # Collecting the id's of the token which appear only once
        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.items() if docfreq == 1]

        # Removing the unwanted tokens using collected id's
        self.dictionary.filter_tokens(stop_ids + once_ids)

        self.dictionary.save(os.path.join('data', 'dictionary.dict'))  # store the dictionary, for future reference

        # Save vocabulary
        vocFile = open(os.path.join('data', 'vocabulary.dat'), 'w',encoding='utf-8')
        for word in self.dictionary.values():
            vocFile.write(word + '\n')

        vocFile.close()

        print('Dictionary and vocabulary saved')


class DTModeller:
    def make_dtm(self):
        # Make DTM
        os.system('dtm-win64.exe ./main --ntopics=5 --mode=fit --rng_seed=12000 --initialize_lda=true --corpus_prefix=data/ --outname=data/output --top_chain_var=0.9 --alpha=0.01 --lda_sequence_min_iter=1 --lda_sequence_max_iter=3 --lda_max_em_iter=4')

            # Import to tethne
        self.dtm = dtmmodel.from_gerrish('data/output/', 'data/metadata.dat', 'data/vocabulary.dat')




    def writeTopics(self,numtimes,months):

        files=['OutputDTM0.csv','OutputDTM1.csv','OutputDTM2.csv','OutputDTM3.csv','OutputDTM4.csv']

        for i in range(5):

            with open(files[i], 'w',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                # Write header
                writer.writerow(['TopicID', 'Word', 'Year', 'Probability'])

                for year_i in range(numtimes):

                    arr = self.dtm.print_topic(i, year_i, 5)  # returns the top 5 words for topic 0 in time 0
                    # my code
                    word_arr = []

                    count_prob = 0
                    for ele in arr:
                        word_arr.append(ele[0])
                        # word_str=word_str+ele[0]
                        count_prob = count_prob + ele[1]
                    word_str = ' '.join(word_arr)
                    writer.writerow([int(i), word_str, months[year_i], count_prob])


        print("done everything")

class Handler:
    def __init__(self,storeFolder=None,start=None,end=None):
        self.path=storeFolder
        #self.start_date = int((start.split('-')[-1]))
        #self.end_date =int((end.split('-')[-1]))
        self.times=["201810","201811","201812","201901","201902","201903","201904"]
        self.months = {"201810":"October 2018","201811":"November 2018","201812":"Decemebr 2018","201901":"January 2019","201902":"February 2019","201903":"March 2019","201904":"April 2019"}
        self.start = self.times.index(start)
        self.end = self.times.index(end)

    def handle(self):

        self.timestamps=[]
        self.monthstamps=[]


        for month in range(self.start , self.end+1):
            self.timestamps.append(self.times[month])
            self.monthstamps.append(self.months[self.times[month]])
        print(self.timestamps)

        FileMaker(path=self.path,timestamps=self.timestamps).writeToFiles()

        mymodel= DTModeller()
        mymodel.make_dtm()
        #mymodel.writeTopics(numtimes=len(self.timestamps))
        mymodel.writeTopics(numtimes=len(self.timestamps),months=self.monthstamps)




