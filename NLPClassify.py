import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Embedding, LSTM, GRU, Convolution1D, Flatten, Dropout
from keras.layers.embeddings import Embedding
import pickle
import csv

for k in range(9, 10):
	with open('tokenizer3.pickle', 'rb') as handle:
	    tokenizer_obj = pickle.load(handle)

	df = pd.DataFrame()
	if(k < 10):
		num = "0" + str(k)
	else:
		num=str(k)
	date = "RC_2015-"+num
	df = pd.read_csv('../Reddit-Parsed.csv', encoding='utf-8')
	df.fillna("none",inplace=True)
	#df = pd.read_csv('../research/NOVEMBER2017DATA/incelsNovemberWeek0.csv', encoding='utf-8')
	# df2 = pd.DataFrame()
	# df2 = pd.read_csv('jigsawtoxic/test_labels.csv')


	# df1 = pd.DataFrame()
	# df1 = pd.read_csv('jigsawtoxic/test.csv')


	labels = ['toxic']


	rows = df.loc[:,:].values
	wanted = df.loc[:,"body"].values
	print(wanted.shape)




	json_file = open('model3.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("model3.h5")
	print("Loaded model from disk")
	csvwriter = csv.writer(open(date+'-toxic.csv', 'w', encoding="utf-8"))
	#csvwriter = csv.writer(open('test.csv', 'w', encoding="utf-8"))
	row = ["id","parent_id", "link_id", "subreddit", "author", "body","created_utc","toxicity"]
	csvwriter.writerow(row)
	temp = []
	for i in range(len(wanted)):
		wants = tokenizer_obj.texts_to_sequences([str(wanted[i])])
		temp.append(pad_sequences(wants, maxlen=1403, padding='post')[0])
	temp = np.asarray(temp)
	results = []
	j=0
	while j < len(temp)-1024:
		res = np.asarray(loaded_model.predict(temp[j:j+1024], batch_size=1024))
		results += list(res)
		j+=1024
		print(j)
	last_batch = j
	if(last_batch < len(temp)):
		res = np.asarray(loaded_model.predict(temp[last_batch:], batch_size = 1024))
		results += list(res)
	temp = rows.tolist()
	#print(results)
	num_toxic = 0
	total = 0
	thresh = 0.4
	for i in range(len(results)):

		a = temp[i]
		if(a[0] !="none"):
			#print(a[0])
			discount = 1
			score = 0
			if(results[i] > thresh):
				a.append(1)
				num_toxic+=1
				#print(a[5])
			else:
				a.append(0)
			total+=1
			if(score > 2): 
				#print(score)
				#print(a)
				pass
			csvwriter.writerow(a)
		
	print(total, num_toxic)