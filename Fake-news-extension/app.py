# importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
from flask import jsonify
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from stemmer import Stemmer
import json

warnings.filterwarnings('ignore')



def loadModels(modelDir, vectorizerDir):
    with open(modelDir, "rb") as f:
        model = pickle.load(f)

    with open(vectorizerDir, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

def predictLogistic(inputs : list[list]):
    model, vectorizer = loadModels( "./model/model.pkl", 
        "./model/vectorizer.pkl")

    stemmed_data = Stemmer().fit_transform(inputs)
    X = vectorizer.transform(stemmed_data.astype('U'))
    
    return model.predict(X)



app = Flask(__name__)


@app.route("/fake-news/predict", methods=["POST"])
def predict():
    data = request.get_json()

    print(data)

    content = data['content']
    content = np.asarray(content)

    preds = predictLogistic(content)
    preds = list(map(int, preds))
    
    return json.dumps({ "predictions" : preds })


if __name__ == "__main__":
    app.run(debug=True)
