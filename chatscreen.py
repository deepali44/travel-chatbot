from tkinter import *                       
from random import choice
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
import speech_recognition as sr
import pickle

data = pickle.load( open( "training_data", "rb" ) )

words = data['words']

classes = data['classes']

train_x = data['train_x']

train_y = data['train_y']



import json

with open('intents.json') as json_data:

    intents = json.load(json_data)


net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


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


model.load('./model.tflearn')

context = {}
ERROR_THRESHOLD = 0.25
def classify(sentence):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        return (random.choice(i['responses']))

            results.pop(0)
'''
print("Start chatting with our chatbot")
ch = int(input("Choose 1.Text 2.Speech"))
if(ch == 1):    
    print("Hello")
    while(True):
        p = input("you : ")
        print("Bot : "+response(p))

if(ch == 2):
    while(True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Ask question our chatbot!")
            audio = r.listen(source)
         
        # Speech recognition using Google Speech Recognition
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            print("You said: " + r.recognize_google(audio))
            print("bot:"+(response(r.recognize_google(audio))))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))



'''
def recog():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
         
        # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        user.set(r.recognize_google(audio))
        bot.set((response(r.recognize_google(audio))))
    except sr.UnknownValueError:
        bot.set("Sorry i did not get that. Can you repeat it")
    except sr.RequestError as e:
        bot.set("Could not request results from Google Speech Recognition service; {0}".format(e))
                                    
ask   = ["hi", "hello"]                         
hi    = ["hi", "hello", "Hello too"]                    
error = ["sorry, i don't know", "what u said?" ]            
                                                                    
root = Tk()                             
user = StringVar()                          
bot  = StringVar()                          
                                                  
                            
label = Label(root, text="Travel chatbot : Tensor",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
label.pack(side="top", pady=(30,10))


label2=Label(root,text="User",width=20,height=1,fg="black",font=('robotic',20,'bold'))
label2.pack(side="top", pady=20)

entry1 = Entry(root,relief="sunken",bd=3,validate="key",insertwidth=4,textvariable=user,width=100)
entry1.pack(side = "top", pady="10")

label1=Label(root,text="Tensor",width=20,height=2,fg="black",font=('robotic',0,'bold'))
label1.pack(side="top", pady=20)

entry2 = Entry(root,relief="sunken",bd=3,validate="key",insertwidth=100,textvariable=bot,width=140)

        

entry2.pack(side = "top", pady="10")
def main():                             
       question = user.get()                                          
       bot.set(response(question))                                    
                                
Button(root, text="ask", command=main).pack(side = "top", pady="20")        
b=Button(root, text="speak", command=recog).pack(side = "top", pady="20")                                   
mainloop()
