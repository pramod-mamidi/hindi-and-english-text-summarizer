from django.shortcuts import render
import numpy as np
import sys
import pandas as pd
import nltk
import re
import codecs
from hindi_summarizer.sent_segment import sent_tokenize
from hindi_summarizer.word_segment import Tokenizer
from bs4 import BeautifulSoup as bs
import requests as r
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import json
#from hindi_summarizer.w2v import vocab
def main(l):
    try:
        if(l[0:12]=="https://www."):
            all_of_it=""
            req=r.get(l)
            con=req.content
            soup=bs(con,'html.parser')
            txt=soup.find_all('p')
            for i in txt:
                all_of_it+=i.text
        else:
            all_of_it=l
        print(all_of_it)
        out=re.split(',|\.|\|',all_of_it)
        sentences = sent_tokenize(all_of_it)
        with open('hindi_summarizer\Aembed_hin.json',encoding='utf8') as f:
            word_embeddings=json.load(f)
        vectors=[]
        l=[]
        [l.append(0) for i in range(100)]
        for i in sentences:
            if len(i) != 0:
                v = sum([np.array(word_embeddings.get(w,l)) for w in i])/(len(i)+0.001)
            else:
                v = np.zeros((100,))
            vectors.append(v)
        print(vectors)
        mat = np.zeros([len(sentences), len(sentences)])
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    mat[i][j] = cosine_similarity(vectors[i].reshape(1,100),vectors[j].reshape(1,100))[0,0]
        nx_graph = nx.from_numpy_array(mat)
        hubs,scores = nx.hits(nx_graph,max_iter=100000000000000000000000000000000000)
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(out)), reverse=True)
        c=0
        s=""
        inl=[]
        k=0.2*len(out)
        for i in ranked_sentences:
            c+=1
            s+=i[1]+'|'
            if(c>k):
                break
        inl.append(s)
        inl.append(all_of_it)
        return inl
    except:
        inl=[]
        inl.append("Sorry for the inconvenience our backend does not support articles with bad encoding patterns please try with other websites or try copy pasting text instead of giving the link")
        inl.append(l)
        return(l)
