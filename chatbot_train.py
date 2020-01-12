import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import scipy
import pandas
import tflearn
import tensorflow as tf
import random
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

words = []

classes = []

documents = []

ignore_words = ['?',',','.',',','!']


for intent in intents['intents']:

    for pattern in intent['patterns']:


        w = nltk.word_tokenize(pattern)


        words.extend(w)


        documents.append((w, intent['tag']))


        if intent['tag'] not in classes:

            classes.append(intent['tag'])




words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]

words = sorted(list(set(words)))




classes = sorted(list(set(classes)))



print (len(documents), "documents")

print (len(classes), "classes", classes)

print (len(words), "unique stemmed words", words)

training = []

output = []


output_empty = [0] * len(classes)




for doc in documents:


    bag = []


    pattern_words = doc[0]


    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]


    for w in words:

        bag.append(1) if w in pattern_words else bag.append(0)




    output_row = list(output_empty)

    output_row[classes.index(doc[1])] = 1



    training.append([bag, output_row])




random.shuffle(training)

training = np.array(training)




train_x = list(training[:,0])

train_y = list(training[:,1])
print(train_x)
print(train_y)

tf.reset_default_graph()


net = tflearn.input_data(shape=[None, len(train_x[0])])

net = tflearn.fully_connected(net, 8)

net = tflearn.fully_connected(net, 8)

net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')

net = tflearn.regression(net)




model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


model.fit(train_x, train_y, n_epoch=800, batch_size=8, show_metric=True)

model.save('model.tflearn')





def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))
p = bow("is your shop open today?", words)
print (p)
print (classes)

import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )
print(model.predict([p]))
