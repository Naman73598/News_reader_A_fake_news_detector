import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import TransformerMixin
from sklearn.base import BaseEstimator
import numpy as np

class Stemmer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.port_stem = PorterStemmer()
        nltk.download('stopwords')
        nltk.download('punkt')

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        stemmed_X = []

        for content in X:
            stemmed_content = re.sub('[^a-zA-Z]',' ',content)
            stemmed_content = stemmed_content.lower()
            stemmed_content = stemmed_content.split()
            stemmed_content = [self.port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
            stemmed_content = ' '.join(stemmed_content)
            stemmed_X.append(stemmed_content)
        return np.asarray(stemmed_X)
    
    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)