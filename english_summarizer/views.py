from django.shortcuts import render
import numpy as np
import sys
import pandas as pd
import nltk
import re
import networkx as nx
from nltk.tokenize import sent_tokenize
import requests as r
from bs4 import BeautifulSoup as bs
from sklearn.metrics.pairwise import cosine_similarity

def main(l):
    vectors = []
    word_embeddings = {}
    sentences=[]
    nltk.download('punkt')
    nltk.download('stopwords')
    if(l[0:8]=="https://"):
        all_of_it=""
        req=r.get(l)
        con=req.content
        soup=bs(con,'html.parser')
        txt=soup.find_all('p')
        for i in txt:
            all_of_it+=i.text
    else:
        all_of_it=l
    sentences.append(sent_tokenize(all_of_it))
    sentences = [y for x in sentences for y in x]
    f = open('english_summarizer/glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()
    csentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    csentences = [s.lower() for s in csentences]
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    def remove_stopwords(sen):
        snew = " ".join([i for i in sen if i not in stop_words])
        return snew
    csentences = [remove_stopwords(r.split()) for r in csentences]
    for i in csentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        vectors.append(v)
    mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                mat[i][j] = cosine_similarity(vectors[i].reshape(1,100),vectors[j].reshape(1,100))[0,0]

    graph = nx.from_numpy_array(mat)
    scores = nx.pagerank(graph)

    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    c=0
    a=""
    inl=[]
    for i in ranked_sentences:
        if "collect" in (i[1]) or "data" in (i[1]) or "use" in (i[1])  or "access" in (i[1]) or "time" in i[1] and "party" in (i[1]):
            a+=i[1]+'\n'
            c+=1
        if c==9:
            break
    inl.append(a)
    inl.append(all_of_it)
    return inl
