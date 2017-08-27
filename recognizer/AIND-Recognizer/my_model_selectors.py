import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        bic_score = [] 
        for ns in range(self.min_n_components, self.max_n_components + 1):
            try:
               model = self.base_model(ns)
               log_likelihood = model.score(self.X, self.lengths)
               n_data_pt = len(self.sequences)
               n_feature = len(self.sequences[0])
               n_param = ns**2 + 2*ns*n_feature - 1
               bic = (-2 * log_likelihood) + (n_param*np.log(n_data_pt))
               bic_score.append((ns, bic))
            except Exception:
                pass
        if len(bic_score) != 0:
            opt_ns = min(bic_score, key = lambda item:item[1])[0]
            return  self.base_model(opt_ns)
        else:
            return None

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    '''
    1. Iterate through the number of states
    2. DIC = model's log-likelihood with current word - mean(model's log-likelihood with all the other words)
    3. The bigger the better
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        dic_list = []
        for ns in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(ns)
                this_word_score = model.score(self.X, self.lengths)
                other_words_mean_score = np.mean([model.score(self.hwords[w][0], self.hwords[w][1]) for w in self.hwords if w != self.this_word])
                dic = this_word_score - other_words_mean_score
                dic_list.append((ns,dic))
            except Exception:
                pass
        if len(dic_list) != 0:
            opt_ns = max(dic_list, key = lambda item:item[1])[0]
            return  self.base_model(opt_ns)
        else:
            return None


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        '''
        Outline
        -----------

        Outter Loop) 
        1. The range of possible number of states is from min_n_components to max_n_components
        2. Loop through min to max, find the best number of state that gives the highest log-likelihood
        3. log-likelihood is returned by .score(X, lengths) method in GaussianHMM

        Inner loop)
        4. Just doing above iterations could result the "overfitting" and that's when KFold comes into play.
        5. The group of sampled data of a word (returned by get_word_sequences) is divided by K (3 by default)
        6. This will be the interal iteration under the number_of_state iteration. Meaning, this is done for each number of model cases.
        7. Train with K-1 data by..
            1) combine_sequences(split_index_list, sequences) will return (X, Xlengths)
            1) modifying self.X and self.lengths with K-1 dataset
            2) call self.base_model(# of states). This will create new GaussianHMM object which calls the "fit" (the training method) upon creation.
        8. Now we have the GaussianHMM model with only K-1 dataset, we evaluate (run .score(X, Lengths)) by feeding the test K data.
        9. Store the output log-likelihood from above to an array, so at the end of the inner loop, we can average them.
        
        Outter loop)
        10. Store the inner loop's averaged log-likelihood to a list

        Return)
        11. Return the model with the optimal number of states

        '''
        
        score_per_n = [] 
        for ns in range(self.min_n_components, self.max_n_components + 1):
            try:
                score_per_k = []
                if len(self.sequences) < 2:
                    model = self.base_model(ns)
                    #score_per_k.append(model.score(self.X, self.lengths))
                    avg_per_k = model.score(self.X, self.lengths)
                else:
                    if len(self.sequences) == 2:
                        kf = KFold(n_splits=2)
                    else:
                        kf = KFold()

                    for train_idx, test_idx in kf.split(self.sequences):
                        self.X, self.lengths = combine_sequences(train_idx, self.sequences)
                        model = self.base_model(ns)
                        test_X, test_X_lengths = combine_sequences(test_idx, self.sequences)
                        score_per_k.append(model.score(test_X, test_X_lengths))

                    avg_per_k = np.mean(score_per_k)
                score_per_n.append((ns, avg_per_k))
            except Exception:
                pass
        if len(score_per_n) != 0:
            opt_ns = max(score_per_n, key = lambda item:item[1])[0]
            return self.base_model(opt_ns)
        else:
            return None
   

        

                