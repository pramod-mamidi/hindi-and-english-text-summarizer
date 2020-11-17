import codecs
import re
from hindi_summarizer.word_segment import Tokenizer
def sent_token(filename):
    f=codecs.open(filename,encoding='utf-8')
    s=[]
    for text in f:
        text=re.sub(r'(\d+)',r'',text)
        text=re.sub(r'(\d+)',r'',text)
        text=text.replace(',','')
        text=text.replace('"','')
        text=text.replace('(','')
        text=text.replace(')','')
        text=text.replace('"','')
        text=text.replace(':','')
        text=text.replace("'",'')
        text=text.replace("‘‘",'')
        text=text.replace("’’",'')
        text=text.replace("''",'')
        text=text.replace(".",'')
        text=text.replace('\n','')
        text=text.replace('\u200d','')
        text=text.replace('\r','')
        text=text.replace('\t','')
        text=text.replace('[0-9]','')
        text=text.replace('IST','')
        text=text.replace('PM','')
        text=text.replace('AM','')
        s.append(text)
    return(s)
def sent_tokenize(data):
    cs=[]
    lis=re.split(',|\.|\|',data)
    for i in range(len(lis)):
        t=Tokenizer(lis[i])
        t.generate_sentences()
        t.tokenize()
        f=t.generate_freq_dict()
        f=t.generate_stem_dict()
        z=t.remove_stop_words()
        cs.append(t.final_tokens)
    return cs

#sent_tokenize("लेकिन ऐसा क्यों होता है ? इसका जवाब खोजते समय 27 सितंबर 1994 की उस घटना पर ध्यान देना चाहिए जिसमें 852 लोग समुद्र में डूब गए थे.उस दिन सुबह सात बजे समुद्री जहाज़ एमएस एस्टोनिया 989 मुसाफ़िरों को लेकर तालिन बंदरगाह से रवाना हुआ. उसे बाल्टिक सागर पार कर स्टॉकहोम जाना था. पर जहाज़़ कभी वहाँ नहीं पंहुचा.बंदरगाह छोड़ने के छह घंटे बाद जहाज़ ज़बरदस्त तूफ़ान में फंस गया, इसके सामने का दरवाज़ा टूट गया और पानी तेज़ी से अंदर घुसने लगा.घंटे भर में जहाज़ डूब गया और इसके साथ ही डूब गए 852 यात्री और जहाज़ का चालक दल.")
