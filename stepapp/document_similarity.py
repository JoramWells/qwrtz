import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


# Measuring the relevancy of a word in a document quantify word in a document
# Compute weight to each word
# VECTORING THE WORD CORPUS

# Adding stop-words
stop_words = set(stopwords.words('english'))



def read_data(path):
	data = pd.read_csv(path)
	return data

# term = keys
# inverse
# document = dataframe
# frequency=frequency,default(1)

def tf_idf(keys, dataframe, label, frequency=1):

	# create a tfidf object
	tfidf_vectorizer = TfidfVectorizer()

	#Term frequency : tf(t,d) = count of t in d / number of words in d

	tfidf_matrix = tfidf_vectorizer.fit_transform(dataframe.loc[:, label].values.astype('U'))

	query = tfidf_vectorizer.transform([keys])
	print(query)
	cs = cosine_similarity(query, tfidf_matrix)
	print(cs)
	similarity_list = cs[0]
	print(similarity_list)
	result_list = []
	r_list =[]
	while frequency > 0:
		tmp_index = np.argmax(similarity_list)
		result_list.append(tmp_index)
		similarity_list[tmp_index] = 0
		
		# Decrement the frequency
		frequency -= 1
  
	print("result_list: %s"%result_list)
	for i in result_list:
		if i == 0:
			break
		else:
			r_list.append(i)
			
			print(r_list)
		
	print(" ".join(str(v) for v in r_list))
	return r_list
