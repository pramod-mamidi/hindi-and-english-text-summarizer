import codecs
import re
class Tokenizer():

	def __init__(self,text=None):
		if text is  not None:
			self.text=text
			self.clean_text()
		else:
			self.text=None
		self.sentences=[]
		self.tokens=[]
		self.stemmed_word=[]
		self.final_list=[]
		#self.final_tokens=[]


	def read_from_file(self,filename):
		f=codecs.open(filename,encoding='utf-8')
		self.text=f.read()
		self.clean_text()



	def generate_sentences(self):
		text=self.text
		self.sentences=re.split(",|\.|\|",text)

	def print_sentences(self,sentences=None):
		if sentences:
			for i in sentences:
				print(i.encode('utf-8'))
		else:
			for i in self.sentences:
				print(i.encode('utf-8'))


	def clean_text(self):
		text=self.text
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
		self.text=text

	def remove_only_space_words(self):

		tokens=[tok for tok in self.tokens if tok.strip()]
		self.tokens=tokens

	def hyphenated_tokens(self):

		for each in self.tokens:
			if '-' in each:
				tok=each.split('-')
				self.tokens.remove(each)
				self.tokens.append(tok[0])
				self.tokens.append(tok[1])



	def tokenize(self):
		if not self.sentences:
			self.generate_sentences()

		sentences_list=self.sentences
		tokens=[]
		for each in sentences_list:
			word_list=each.split(' ')
			tokens=tokens+word_list
		self.tokens=tokens
		#remove words containing spaces
		self.remove_only_space_words()
		#remove hyphenated words
		self.hyphenated_tokens()

	def print_tokens(self,print_list=None):
		if print_list is None:
			for i in self.tokens:
				print(i)
		else:
			for i in print_list:
				print(i)


	def tokens_count(self):
		return len(self.tokens)

	def sentence_count(self):
		return len(self.sentences)

	def len_text(self):
		return len(self.text)

	def concordance(self,word):
		if not self.sentences:
			self.generate_sentences()
		sentence=self.sentences
		concordance_sent=[]
		for each in sentence:
			each=each
			if word in each:
				concordance_sent.append(each.decode('utf-8'))
		return concordance_sent

	def generate_freq_dict(self):
		freq={}
		if not self.tokens:
			self.tokenize()

		temp_tokens=self.tokens
		#doubt whether set can be used here or not
		for each in self.tokens:
			freq[each]=temp_tokens.count(each)

		return freq

	def print_freq_dict(self,freq):
		for i in list(freq.keys()):
			print(i.encode('utf-8'),',',freq[i])

	def generate_stem_words(self,word):
		suffixes = {
    1: ["ो","े","ू","ु","ी","ि","ा"],
    2: ["कर","ाओ","िए","ाई","ाए","ने","नी","ना","ते","ीं","ती","ता","ाँ","ां","ों","ें"],
    3: ["ाकर","ाइए","ाईं","ाया","ेगी","ेगा","ोगी","ोगे","ाने","ाना","ाते","ाती","ाता","तीं","ाओं","ाएं","ुओं","ुएं","ुआं"],
    4: ["ाएगी","ाएगा","ाओगी","ाओगे","एंगी","ेंगी","एंगे","ेंगे","ूंगी","ूंगा","ातीं","नाओं","नाएं","ताओं","ताएं","ियाँ","ियों","ियां"],
    5: ["ाएंगी","ाएंगे","ाऊंगी","ाऊंगा","ाइयाँ","ाइयों","ाइयां"],
}
		for L in 5, 4, 3, 2, 1:
			if len(word) > L + 1:
				for suf in suffixes[L]:
					#print type(suf),type(word),word,suf
					if word.endswith(suf):
						#print 'h'
						return word[:-L]
		return word

	def generate_stem_dict(self):
		'''returns a dictionary of stem words for each token'''
		stem_word={}
		if not self.tokens:
			self.tokenize()
		for each_token in self.tokens:
			#print type(each_token)
			temp=self.generate_stem_words(each_token)
			#print temp
			stem_word[each_token]=temp
			self.stemmed_word.append(temp)

		return stem_word

	def remove_stop_words(self):
		f=codecs.open("hindi_summarizer\stopwords.txt",encoding='utf-8')
		if not self.stemmed_word:
			self.generate_stem_dict()
		stopwords=[x.strip() for x in f.readlines()]
		tokens=[i for i in self.stemmed_word if str(i) not in stopwords]
		self.final_tokens=tokens
		return tokens


if __name__=="__main__":
	t=Tokenizer('''वाशिंगटन: दुनिया के सबसे शक्तिशाली देश के राष्ट्रपति बराक ओबामा ने प्रधानमंत्री नरेंद्र मोदी के संदर्भ में 'टाइम' पत्रिका में लिखा, "नरेंद्र मोदी ने अपने बाल्यकाल में अपने परिवार की सहायता करने के लिए अपने पिता की चाय बेचने में मदद की थी। आज वह दुनिया के सबसे बड़े लोकतंत्र के नेता हैं और गरीबी से प्रधानमंत्री तक की उनकी जिंदगी की कहानी भारत के उदय की गतिशीलता और क्षमता को परिलक्षित करती है।''')
	t.generate_sentences()
	t.tokenize()
	f=t.generate_freq_dict()
	s=t.concordance('बातों')
	f=t.generate_stem_dict()
	z=t.remove_stop_words()
	t.print_tokens(t.final_tokens)
	print(t.sentence_count(),t.tokens_count(),t.len_text())
