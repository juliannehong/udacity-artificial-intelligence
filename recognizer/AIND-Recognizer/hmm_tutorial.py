import numpy as np
from hmmlearn import hmm

np.random.seed(42)

model = hmm.GaussianHMM(n_components=3, covariance_type="full")
model.startprob = np.array([0.6, 0.3, 0.1])
