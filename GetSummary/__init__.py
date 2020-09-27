import logging
import nltk
import json
nltk.download('stopwords')
nltk.download('wordnet') 

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    def get_sentences(text: str) -> list:
        sentence_array = text.split(". ")
        sentences = []

        for sentence in sentence_array:
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()

        return sentences

    def sentence_similarity(sentence_1: str, sentence_2: str, stopwords: list = None) -> float:
        if stopwords is None:
            stopwords = []
    
        sentence_1 = [w.lower() for w in sentence_1]
        sentence_2 = [w.lower() for w in sentence_2]
    
        all_words = list(set(sentence_1 + sentence_2))
    
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
    
        for w in sentence_1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
    
        for w in sentence_2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
    
        return 1 - cosine_distance(vector1, vector2)

    def build_similarity_matrix(sentences: list, stop_words: list) -> np.array:
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue 
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix

    def generate_summary(text: str, top_n: int) -> str:
        stop_words = stopwords.words('english')
        summarize_text = []

        sentences = get_sentences(text)

        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    

        for i in range(min(top_n, len(ranked_sentence))):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        return '. '.join(summarize_text) + '.'

    req_body = req.get_json()

    data = {
        'summary': generate_summary(req_body.get('text'), req_body.get('sentences'))
    }

    return func.HttpResponse(body = f'{json.dumps(data)}', status_code = 200)
