
'''Classes and methods related to the :class:`.DTMModel`\.'''


import numpy as np
import os
import re
import csv
import sys
from operator import  itemgetter
PYTHON_3 = sys.version_info[0] == 3
if PYTHON_3:
    unicode = str



import sys
if sys.version_info[0] > 2:
    xrange = range
    
# Logging.
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


from dtm_init import Model


class DTMModel(Model):
    """
    Represents a Dynamic Topic Model (DTM).
    
    The DTM is similar to the LDA model (see :class:`.LDAModel`) except that
    each topic is permitted to evolve over time (i.e. probabilities associated
    with terms in the topic can change). For a complete description of the model
    see `Blei & Lafferty 2006 <http://www.cs.cmu.edu/~lafferty/pub/dtm.pdf>`_.
    
    To generate a :class:`.DTMModel` from a :class:`.Corpus` use the
    :class:`.DTMModelManager`\, which relies on S. Gerrish's `C++ implementation
    of DTM <http://code.google.com/p/princeton-statistical-learning/downloads/detail?name=dtm_release-0.8.tgz>`_. Alternatively, you can build the
    model externally (e.g. using the Gerrish DTM implementation directly), and
    then load the results with :func:`.from_gerrish`\.
    
    If you are using a different implementation of DTM, you can initialize a
    :class:`.DTMModel` directly by providing parameters and metadata.
    
    * ``e_theta`` should describe the distribution of topics (rows) in documents 
      (cols).
    * ``phi`` should describe the topic (dimension 0) distributions over words
      (dimension 1) over time (dimension 2).
    * ``metadata`` should map matrix indices for documents onto :class:`.Paper`
      IDs (or whatever you use to identify documents).
    * ``vocabulary`` should map matrix indices for words onto word-strings.
    
    .. autosummary::
       :nosignatures:
       
       list_topic
       list_topics
       topic_evolution
       print_topic
       print_topics
    
    Parameters
    ----------
    e_theta : matrix-like
        Distribution of topics (Z) in documents (M). Shape: (Z, M).
    phi : matrix-like
        Topic (Z) distribution over words (W), over time (T). Shape: 
        (Z, W, T)
    metadata : dict
        Maps matrix indices onto document datadata.
    vocabulary : dict
        Maps W indices onto words.
    """

    def __init__(self, e_theta, phi, metadata, vocabulary):
        """
        Initialize the :class:`.DTMModel`\.
        """
        
        self.e_theta = e_theta
        self.Z = e_theta.shape[0]   # Number of topics. #shape gives the dimension------rows
        self.M = e_theta.shape[1]   # Number of documents.------col.s
        
        self.phi = phi

        print(self.phi)

        self.W = phi.shape[1]    # Number of words.

        self.T = phi.shape[2]    # Number of time periods.   #

        self.metadata = metadata
        self.vocabulary = vocabulary

        self.lookup = { v['id']:k for k,v in metadata.items() }
        print(self.lookup)
    
        logging.info('DTMModel.__init__(): loaded model with' + \
                      ' {0} topics, {1} documents,'.format(self.Z, self.M) + \
                      ' {0} words, {1} time periods.'.format(self.W, self.T))

    def _item_description(self, i, **kwargs):
        """
        Proportion of each topic in document.
        """
        
        return [ (k, self.e_theta[k, i]) 
                    for k in xrange(self.e_theta[:, i].size) ]
        

    def _dimension_description_new(self, k, w ):
        dictionary=self.vocabulary
        word_to_index=list(dictionary.keys())[list(dictionary.values()).index(w)]

        """
        Yields probability distribution over terms.
        """

        a=[ (t, self.phi[k, word_to_index, t])
                    for t in range(4) ] # probabilities of each word in vocabulary for topic 0 in time stamp 0

        return a
        
    def _dimension_description(self, k, t, **kwargs):
        

        """
        Yields probability distribution over terms.
        """
        a=[ (w, self.phi[k, w, t])
                    for w in xrange(self.phi[k, :, t].size) ] # probabilities of each word in vocabulary for topic 0 in time stamp 0

        #print(self.phi)

        '''
        self.phi-> rows are words in vocab. col.s are timestamps
        
      [ [[P t0 , P t1, P t2, P t3]
         [                       ]
         ...
         [                       ]
         [                       ]] , 
         
         [[P t0 , P t1, P t2, P t3]
         [                       ]
         ...
         [                       ]
         [                       ]]  ]
        
        '''
        ###################################### my code

        sorted_by_probabilities=sorted(a, key=itemgetter(1))# itemgetter is faster - list gets sorted from lowest to highest probabilities
        #print(len(sorted_by_probabilities),sorted_by_probabilities)
        
        res=sorted_by_probabilities[-5:]   # last 5 elements in the list has the highest probabilities.
        #print(len(res),res)
        return  res

        #most_common_10 =(dict(Counter(a).most_common(10)))
        #return most_common_10
        
    def _dimension_items(self, k, threshold, **kwargs):
        """
        Returns items that contain ``k`` at or above ``threshold``.
        
        Parameters
        ----------
        k : int
            Topic index.
        threshold : float
            Minimum representation of ``k`` in document.
            
        Returns
        -------
        description : list
            A list of ( item, weight ) tuples.
        """


        description = [ (self.metadata[i]['id'], self.e_theta[k,i])
                            for i in xrange(self.e_theta[k,:].size)
                            if self.e_theta[k,i] >= threshold ]
        return description
    

    def topic_evolution(self, k, Nwords):
        """
        Generate a plot that shows p(w|z) over time for the top ``Nwords``
        terms.
        
        Parameters
        ----------
        k : int
            A topic index.
        Nwords : int
            Number of words to return.
            
        Returns
        -------
        keys : list
            Start-date of each time-period.
        t_series : list
            Array of p(w|t) for Nwords for each time-period.
        """
        #self.T=#no.of timestamps=4
        t_keys = range(self.T)
        #with open('testtext.txt', 'a') as tf:
          # tf.write(str(self.phi))

        t_values = {}
        t_val={}
        for t in t_keys:

            dim = self._dimension_description(k, t=t, Nwords=5)
            #with open('testtext.txt', 'a') as tf:
                 #tf.write(str(dim))
            for ele in dim:
                w=ele[0]
                p=ele[1]
                if w not in t_values:
                    t_values[w] = {}
                t_values[w][t] = p   #probability of a word in timestamp t




        t_series = {}
        for w, values in t_values.items():#for each word { 0: { 0:p0, 1:p1, 2:p2, 3:p3 } ,{},.....}
            word = self.vocabulary[w]
            series = []
            for t in t_keys:
                if t in values:
                    series.append(values[t]) #[p0,p1,p2,p3,]
                else:   # No value for that time-period.
                    series.append(0.)
            t_series[word] = series # for each word prob.over times
        # print(dict(Counter(t_values).most_common(5)))
        return t_keys, t_series
    


    def list_topic(self, k, t, Nwords):
        """
        Yields the top ``Nwords`` for topic ``k``.
        
        Parameters
        ----------
        k : int
            A topic index.
        t : int
            A time index.
        Nwords : int
            Number of words to return.
        
        Returns
        -------
        as_list : list
            List of words in topic.
        """
        words = self._dimension_description(k, t=t, top=Nwords)
        as_dict = [ (self.vocabulary[w],p) for w,p in words ]

        return as_dict

    def list_topic_new(self, k, t, Nwords):
        """
        Yields the top ``Nwords`` for topic ``k``.
        
        Parameters
        ----------
        k : int
            A topic index.
        t : int
            A time index.
        Nwords : int
            Number of words to return.
        
        Returns
        -------
        as_list : list
            List of words in topic.
        """
        words = self._dimension_description(k, t=t, top=Nwords)
        as_dict = [ (t,self.vocabulary[w],p) for w,p in words ]

        return as_dict


    def list_topic_diachronic(self, k, Nwords):
        as_dict = { t:self.list_topic(k, t, Nwords)
                        for t in xrange(self.T) }
        return as_dict
        


    def print_topic_diachronic(self, k, Nwords):
        as_dict = self.list_topic_diachronic(k, Nwords)
        s = []
        for key, value in as_dict.iteritems():
            s.append('{0}: {1}'.format(key, ', '.join(value)))
        as_string = '\n'.join(s)
        
        return as_string
    


    def print_topic(self, k, t, Nwords): #k=topic index,
        """
        Yields the top ``Nwords`` for topic ``k``.
        
        Parameters
        ----------
        k : int
            A topic index.
        t : int
            A time index.
        Nwords : int
            Number of words to return.
        
        Returns
        -------
        as_string : str
            Joined list of words in topic.
        """

        as_string = self.list_topic(k, t=t, Nwords=Nwords)
    
        return as_string
    
    def print_topic_new(self, k, t, Nwords): #k=topic index,
        """
        Yields the top ``Nwords`` for topic ``k``.
        
        Parameters
        ----------
        k : int
            A topic index.
        t : int
            A time index.
        Nwords : int
            Number of words to return.
        
        Returns
        -------
        as_string : str
            Joined list of words in topic.
        """

        as_string = self.list_topic_new(k, t=t, Nwords=Nwords)
    
        return as_string
    

    def list_topics(self, t, Nwords):
        """
        Yields the top ``Nwords`` for each topic.
        
        Parameters
        ----------
        t : int
            A time index.
        Nwords : int
            Number of words to return for each topic.
        
        Returns
        -------
        as_dict : dict
            Keys are topic indices, values are list of words.
        """
        
        as_dict = {}
        for k in xrange(self.Z):
            as_dict[k] = self.list_topic(k, t, Nwords)
    
        return as_dict
    


    def print_topics(self, t, Nwords):
        """
        Yields the top ``Nwords`` for each topic.
        
        Parameters
        ----------
        t : int
            A time index.
        Nwords : int
            Number of words to return for each topic.
        
        Returns
        -------
        as_string : str
            Newline-delimited lists of words for each topic.
        """
            
        as_dict = self.list_topics(t, Nwords)
        s = []
        for key, value in as_dict.items():
            s.append('{0}: {1}'.format(key, ', '.join(value)))
        as_string = '\n'.join(s)
        
        return as_string


def from_gerrish(target, metadata, vocabulary, metadata_key='doi'):
    """
    Generate a :class:`.DTMModel` from the output of `S. Gerrish's C++ DTM 
    implementation <http://code.google.com/p/princeton-statistical-learning/downloads/detail?name=dtm_release-0.8.tgz>`_.
    
    The Gerrish DTM implementation generates a large number of data files
    contained in a directory called ``lda-seq``. The ``target`` parameter
    should be the path to that directory.
    
    ``metadata`` should be the path to a tab-delimted metadata file. Those
    records should occur in the same order as in the corpus data files used
    to generate the model. For example::
    
       id	date	atitle
       10.2307/2437162	1945	SOME ECOTYPIC RELATIONS OF DESCHAMPSIA CAESPITOSA
       10.2307/4353229	1940	ENVIRONMENTAL INFLUENCE AND TRANSPLANT EXPERIMENTS
       10.2307/4353158	1937	SOME FUNDAMENTAL PROBLEMS OF TAXONOMY AND PHYLOGENETICS
       
    ``vocabulary`` should be the path to a file containing the words used to
    generate the model, one per line.
    
    Parameters
    ----------
    target : str
        Path to ``lda-seq`` output directory.
    metadata : str
        Path to metadata file.
    vocabulary : str
        Path to vocabulary file.
        
    Returns
    -------
    :class:`.DTMModel`
    """

    e_log_prob = 'topic-{0}-var-e-log-prob.dat'
    info = 'topic-{0}-info.dat'
    obs = 'topic-{0}-obs.dat'

    reader = GerrishLoader(target, metadata, vocabulary)#, metadata, vocabulary)
    return reader.load()

class GerrishLoader(object):
    """
    Helper class for parsing results from `S. Gerrish's C++ implementation <http://code.google.com/p/princeton-statistical-learning/downloads/detail?name=dtm_release-0.8.tgz>`_ 

    Parameters
    ----------
    target : str
        Path to ``lda-seq`` output directory.
    metadata : str
        Path to metadata file.
    vocabulary : str
        Path to vocabulary file.
        
    Returns
    -------
    :class:`.DTMModel`
    """

    def __init__(self, target, metadata_path, vocabulary_path):
        self.target = target
        self.metadata_path = metadata_path
        self.vocabulary_path = vocabulary_path
        
        self.handler = { 'prob': self._handle_prob,
                         'info': self._handle_info,
                         'obs': self._handle_obs     }

        self.tdict = {}




    def load(self):
        try:
            contents = os.listdir(self.target)
            lda_seq_dir = os.listdir('{0}/lda-seq'.format(self.target))
        except OSError:
            raise OSError("Invalid target path.")



        # Metadata.
        self._handle_metadata()
        self._handle_vocabulary()
        
        # Meta-parameters.
        self._handle_metaparams()


        
        # Topic proportions.
        self._handle_gammas()

        # p(w|z)

        for fname in lda_seq_dir:
            #print( fname)
            fs = re.split('-|\.', fname)

            #print(fname, fs)
            #print(fs[1])
            if fs[0] == 'topic':

                z_s = fs[1] #topic num 001
                z = int(z_s) #topic number 1
                self.handler[fs[-2]](fname, z)


        
        #self.tdict.keys()  [0,1,2,3,4]
        print(self.tdict.keys())

   ###############################################################################################################
        '''
        for ele in self.tdict:
            print([ self.tdict[z] for z in range(4) ])
            '''
        tkeys = sorted(self.tdict.keys())

        self.phi = np.array( [ self.tdict[z] for z in tkeys ])

       # for ele in self.phi:
           # print(ele)
        '''
        for ele in self.tdict:
            print([self.tdict[z] for z in range(4)])
            '''


        self.model = DTMModel(self.e_theta, self.phi, self.metadata, self.vocabulary)

        return self.model

    def _handle_metaparams(self):
        # Read metaparameters.
        with open('{0}/lda-seq/info.dat'.format(self.target), 'r',encoding='utf-8') as f:
            for line in f.readlines():
                ls = line.split()
                if ls[0] == 'NUM_TOPICS':
                    self.N_z = int(ls[1])

                elif ls[0] == 'NUM_TERMS':
                    self.N_w = int(ls[1])

                elif ls[0] == 'SEQ_LENGTH':
                    self.N_t = int(ls[1])

                elif ls[0] == 'ALPHA':
                    self.A = np.array(ls[2:])

    def _handle_gammas(self):
        # Read gammas -> e_theta

        #which tweet has most relavane to which topic?
        with open('{0}/lda-seq/gam.dat'.format(self.target), 'r',encoding='utf-8') as f:


            data = np.array(f.read().split())
            #self.N_z= number of desired topics
            self.N_d = data.shape[0]//self.N_z  # 10,935 /5 = 2,187
            b = data.reshape((self.N_d, self.N_z)).astype('float32')

            rs = np.sum(b, axis=1) # sum of gammas of each topic in 5 topics
            self.e_theta = np.array([ b[:,z]/rs for z in xrange(self.N_z) ]) #take first col.divide every entry by sum of first row...

            # self.e_theta = topic proportion of a (word) over the 5 topics

    def _handle_prob(self, fname, z):
        """
        - topic-???-var-e-log-prob.dat: the e-betas (word distributions) for
        topic ??? for all times.  This is in row-major form,
        """

        # topic-000-var-e-log-prob.dat has 6608 entries= prob. of 1652 words * 4 timestamps
        with open('{0}/lda-seq/{1}'.format(self.target, fname), 'r',encoding='utf-8') as f:


            try:
                data = np.array(f.read().split()).reshape((self.N_w, self.N_t))
            except ValueError:
                data = np.array(f.read().split())
            #print(data)
            self.tdict[z] = np.exp(data.astype('float32'))
            #print(self.tdict[z])
            #print('###################################')
            #print(self.tdict[z])




    def _handle_info(self, fname, z):
        """
        No need to do anything with these yet.
        """
        pass

    def _handle_obs(self, fname, z):
        """
        TODO: Figure out what, if anything, this is good for.
        """
        pass

    def _handle_metadata(self):
        """
        
        Returns
        -------
        metadata : dict
            Keys are document indices, values are identifiers from a 
            :class:`.Paper` property (e.g. DOI).
        """
        
        if self.metadata_path is None:
            self.metadata = None
            return
        
        self.metadata = {}

        with open(self.metadata_path, "rU",encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')

            all_lines = [ l for l in reader ]

            keys = all_lines[0]
            lines = all_lines[1:]
            
            i = 0
            for l in lines:
                self.metadata[i] = { keys[i]:l[i] for i in xrange(0, len(l)) }
                i += 1
        return self.metadata

    def _handle_vocabulary(self):
        """
        
        Returns
        -------
        vocabulary : dict
            Keys are word indices, values are word strings.
        """
        if self.vocabulary_path is None:
            raise RuntimeError("No vocabulary provided.")

        # Build vocabulary
        self.vocabulary = {}
        with open(self.vocabulary_path, 'rU',encoding='utf-8') as f:
            i = 0
            for v in f.readlines():
                self.vocabulary[i] = v.strip('\n')
                i += 1
        #print(self.vocabulary)

        return self.vocabulary
