import random
import json
import torch
from model import *
from utils import *

device= torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json','r') as f:
    intents= json.load(f)

FILE='data.pth'
data=torch.load(FILE)

input_size= data['input_size']
hidden_size= data['hidden_size']
output_size= data['output_size']
all_words= data['all_words']
tags= data['tags']
model_state= data['model_state']

model= NeuralNet(input_size,hidden_size,output_size)
model.load_state_dict(model_state)
model.eval()

bot_name='HARRYPOTTER'
print(f'{bot_name}: Lets Chat! Im {bot_name} the bot! How can I help you today? Type "quit" to Exit')

while True:
    sentence=input('You: ')
    if sentence=='quit':
        break

    sentence= tokenize(sentence)
    X= bag_of_words(sentence, all_words)

    X= X.reshape(1,X.shape[0]) #We only have one row because just one sample
    X=torch.from_numpy(X)

    output= model(X)
    _,predicted=torch.max(output, dim=1)  #It gets the Index of maximum prob value
    tag=tags[predicted.item()]    #Gets the corresponding tag

    #Getting the Probability and checking for minimu threshold
    probs= torch.softmax(output, dim=1)
    probs=probs[0][predicted.item()]

    if probs.item() > 0.75:
        for intent in intents['intents']:
            if tag==intent['tag']:
                print(f'{bot_name}: {random.choice(intent["responses"])}')

    else:
        print(f'{bot_name}: I dont understand! Can you try telling it a differently?')
