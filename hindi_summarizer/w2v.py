import nltk
import codecs
from gensim.models import Word2Vec,KeyedVectors
from sent_segment import sent_token
from word_segment import Tokenizer
import numpy as np
import json
def vocab():
        sentences=sent_token('hindi_corpus.txt')
        final_sent=[]
        for i in range(len(sentences)):
            t=Tokenizer(sentences[i])
            t.generate_sentences()
            t.tokenize()
            f=t.generate_freq_dict()
            f=t.generate_stem_dict()
            z=t.remove_stop_words()
            final_sent.append(t.final_tokens)
        model=Word2Vec(final_sent,min_count=1)
        model.wv.save_word2vec_format('Amodel.bin',binary=True)
        #model = KeyedVectors.load_word2vec_format('Amodel.bin', binary=True)
        voc=model.wv.vocab
        embeddings={}
        for i in voc:
            nda=model.wv[i]
            embeddings[i]=nda.tolist()
        with open("Aembed_hin.json","w",encoding='utf8') as fj:
                json.dump(embeddings,fj)
        f = open("Adict.txt","w",encoding='utf8')
        f.write(str(embeddings))
        f.close()

        v=[]
        for i in voc:
            lis=[]
            for j in (model[i]):
                    lis.append(j)
            embed.append(np.array(lis))
            v.append(i)
            embeddings[i]=lis
        f = open("dict.txt","w",encoding='utf8')
        f.write(str(embeddings))
        f.close()
vocab()
