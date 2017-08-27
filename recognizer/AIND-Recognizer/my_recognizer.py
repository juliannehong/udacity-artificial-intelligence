import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer

    '''
    1. iterate through the test_set
    2. per word, iterate through the models, create dictionary {WORD: LogL, ..}, and append to probabailites
    3. pick the word with the highest log-likelihood and append guesses[]
    '''
    for X, lengths in test_set.get_all_Xlengths().values():

      p_dict = {}
      for word, hmm in models.items():
        try:
          p_dict[word] = hmm.score(X, lengths)
        except Exception:
          p_dict[word] = float("-inf")
          continue

      probabilities.append(p_dict)
      guesses.append(max(p_dict, key=p_dict.get))

    return probabilities, guesses
