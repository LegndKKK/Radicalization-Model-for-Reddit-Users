import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, LSTM, GRU, Convolution1D, Flatten, Dropout, MaxPooling1D, Input
from keras.layers.embeddings import Embedding
import pickle



def create_convnet(vocab_size, EMBEDDING_DIM, max_length):
    input_shape0 = Input((max_length,))
    input_shape = Embedding(vocab_size, EMBEDDING_DIM, input_length=max_length)(input_shape0)

    tower_1 = Convolution1D(32, 1, padding='same', activation='relu')(input_shape)
    tower_1 = MaxPooling1D(pool_size=2)(tower_1)

    tower_2 = Convolution1D(32, 2, padding='same', activation='relu')(input_shape)
    tower_2 = MaxPooling1D(pool_size=2)(tower_2)

    tower_3 = Convolution1D(32, 4, padding='same', activation='relu')(input_shape)
    tower_3 = MaxPooling1D(pool_size=2)(tower_3)


    tower_4 = Convolution1D(32, 8, padding='same', activation='relu')(input_shape)
    tower_4 = MaxPooling1D(pool_size=2)(tower_4)

    merged = keras.layers.concatenate([tower_1, tower_2, tower_3, tower_4], axis=1)
    merged = Flatten()(merged)
    out = Dropout(0.8)(merged)
    out = Dense(400, activation='relu')(out)
    out = Dense(1, activation='sigmoid')(out)

    model = Model(input_shape0, out)
    return model


df = pd.DataFrame()
df = pd.read_csv('data/train.csv', encoding='utf-8')


labels = ['toxic']
X_train = df.loc[:80000, 'comment_text'].values
Y_train = df.loc[:80000, labels].values
X_test = df.loc[80001:, 'comment_text'].values
Y_test = df.loc[80001:, labels].values

#print(Y_test[0])

tokenizer_obj = Tokenizer()
total_reviews = X_train#+X_test
tokenizer_obj.fit_on_texts(total_reviews)

max_length = max([len(s.split())for s in total_reviews])
vocab_size = len(tokenizer_obj.word_index)+1
X_train_tokens = tokenizer_obj.texts_to_sequences(X_train)
X_test_tokens = tokenizer_obj.texts_to_sequences(X_test)



# print("hi")
# Y_train_tokens = list()
# Y_test_tokens = list()
# for i in range(len(Y_train)):
#     if Y_train[i] == "positive":
#         Y_train_tokens.append(1)
#     else:
#         Y_train_tokens.append(0)
# for i in range(len(Y_test)):
#     if Y_test[i] == "positive":
#         Y_test_tokens.append(1)
#     else:
#         Y_test_tokens.append(0)
#Y_train_tokens = tokenizer_obj.texts_to_sequences(Y_train)
#Y_test_tokens = tokenizer_obj.texts_to_sequences(Y_test)

X_train_pad = pad_sequences(X_train_tokens, maxlen=max_length, padding='post')
X_test_pad = pad_sequences(X_test_tokens, maxlen=max_length, padding='post')
#print(Y_train_tokens[0])
#print(X_train_pad[0])
print(max_length)
# saving
with open('tokenizer3.pickle', 'wb') as handle:
    pickle.dump(tokenizer_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

EMBEDDING_DIM=100
# model = Sequential()
# model.add(Embedding(vocab_size, EMBEDDING_DIM, input_length=max_length))
# model.add(Convolution1D(64, 3, border_mode='same', activation='relu'))
# model.add(MaxPooling1D(pool_size=2))
# model.add(Flatten())
# model.add(Dense(180,activation='sigmoid'))
# model.add(Dropout(0.8))
# model.add(Dense(6,activation='sigmoid'))
model = create_convnet(vocab_size, EMBEDDING_DIM, max_length)
model.compile(loss="binary_crossentropy", optimizer = "adam", metrics=['accuracy'])
# es = keras.callbacks.EarlyStopping(monitor='val_loss',
#                               min_delta=0,
#                               patience=2,
#                               verbose=0, mode='auto')
model.fit(X_train_pad, Y_train, batch_size=256, epochs=4, validation_data=(X_test_pad, Y_test), verbose=1)
model_json = model.to_json()
with open("model3.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model3.h5")
print("Saved model to disk")
 

