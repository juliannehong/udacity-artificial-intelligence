import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences

from asl_data import AslDb


asl = AslDb() # initializes the database
asl.df.head() # displays the first five rows of the asl database, indexed by video and frame
asl.df['grnd-ry'] = asl.df['right-y'] - asl.df['nose-y']
asl.df['grnd-rx'] = asl.df['right-x'] - asl.df['nose-x']
asl.df['grnd-ly'] = asl.df['left-y'] - asl.df['nose-y']
asl.df['grnd-lx'] = asl.df['left-x'] - asl.df['nose-x']
# collect the features into a list
features_ground = ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']
 #show a single set of features for a given (video, frame) tuple
from my_model_selectors import SelectorConstant

from my_model_selectors import SelectorCV

words_to_train = ['FISH', 'BOOK', 'VEGETABLE', 'FUTURE', 'JOHN']
#words_to_train = ['CHICKEN']
import timeit

# training = asl.build_training(features_ground)  # Experiment here with different feature sets defined in part 1
# sequences = training.get_all_sequences()
# Xlengths = training.get_all_Xlengths()
# for word in words_to_train:
#     start = timeit.default_timer()
#     model = SelectorCV(sequences, Xlengths, word, 
#                     min_n_components=2, max_n_components=15, random_state = 14).select()
#     end = timeit.default_timer()-start
#     if model is not None:
#         print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
#     else:
#         print("Training failed for {}".format(word))
# TODO: Implement SelectorBIC in module my_model_selectors.py
from my_model_selectors import SelectorBIC

# training = asl.build_training(features_ground)  # Experiment here with different feature sets defined in part 1
# sequences = training.get_all_sequences()
# Xlengths = training.get_all_Xlengths()
# for word in words_to_train:
#     start = timeit.default_timer()
#     model = SelectorBIC(sequences, Xlengths, word, 
#                     min_n_components=2, max_n_components=15, random_state = 14).select()
#     end = timeit.default_timer()-start
#     if model is not None:
#         print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
#     else:
#         print("Training failed for {}".format(word))

from my_model_selectors import SelectorDIC

# training = asl.build_training(features_ground)  # Experiment here with different feature sets defined in part 1
# sequences = training.get_all_sequences()
# Xlengths = training.get_all_Xlengths()
# for word in words_to_train:
#     start = timeit.default_timer()
#     model = SelectorDIC(sequences, Xlengths, word, 
#                     min_n_components=2, max_n_components=15, random_state = 14).select()
#     end = timeit.default_timer()-start
#     if model is not None:
#         # print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
#         print (model)
#     else:
#         print("Training failed for {}".format(word))
def train_all_words(features, model_selector):
    training = asl.build_training(features)  # Experiment here with different feature sets defined in part 1
    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    model_dict = {}
    for word in training.words:
        model = model_selector(sequences, Xlengths, word, 
                        n_constant=3).select()
        model_dict[word]=model
    return model_dict
from my_recognizer import recognize
from asl_utils import show_errors

# # TODO Choose a feature set and model selector
features = features_ground # change as needed
model_selector = SelectorCV # change as needed

# # TODO Recognize the test set and display the result with the show_errors method
models = train_all_words(features, model_selector)
test_set = asl.build_test(features)
# #print(models)

# # print (test_set.get_all_sequences()[6])
probabilities, guesses = recognize(models, test_set)
show_errors(guesses, test_set)