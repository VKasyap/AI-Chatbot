import json
from utils import *
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import *

with open('intents.json','r') as f:
    intents= json.load(f)

#print(intents)

all_words=[]
tags=[]
xy=[]

for intent in intents['intents']:
    tag=intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w=tokenize(pattern)  #['Thank', 'you']
        all_words.extend(w)
        #all_words.append(w)    #This would create a list of lists. We dont need that
        xy.append((w,tag))    #[(['Hi'], 'greeting'), (['Hey'], 'greeting'), (['How', 'are', 'you'], 'greeting'),

#Stemming all the words and remove punctuations
ignore_words=['?','!','.',',']
all_words=[stemming(w) for w in all_words if w not in ignore_words]  #['hi', 'hey', 'how', 'are', 'you', 'is', 'anyon', 'there',

all_words= sorted(set(all_words)) #This would sort and rmeove the duplicate values
tags= sorted(tags)  #['delivery', 'funny', 'goodbye', 'greeting', 'items', 'payments', 'thanks']

#print(tags.index('delivery'))  #This would print 0

#Create the Training Data
X_train=[]   #Here we would put the bag of words
y_train=[]

for (pattern_sentence,tag) in xy:
    bag=bag_of_words(pattern_sentence, all_words)  #Patten_sentence are tokenized sentences and all_words are tokenized, stemmed, and sorted
    X_train.append(bag)
    label=tags.index(tag)
    y_train.append(label)

#y_train.type(torch.LongTensor)
X_train= np.array(X_train)   #Its the bag of words in array format
y_train= np.array(y_train)   #Its the Tags in array format


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples=len(X_train)
        self.x_data= X_train
        self.y_data= y_train

    #dataset[idx]
    def __getitem__(self, idx):
        return self.x_data[idx], self.y_data[idx]

    def __len__(self):
        return self.n_samples

#Define the Hyper paramaeters
batch_size=8
hidden_size=8
output_size= len(tags)
input_size= len(all_words)
learning_rate=0.001
num_epochs=1000


dataset= ChatDataset()
train_loader=DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

device= torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model= NeuralNet(input_size,hidden_size,output_size)

#Loss and Optimizer
criterion=nn.CrossEntropyLoss()
optimizer= torch.optim.Adam(model.parameters(), lr= learning_rate )

#Training Loop
for epoch in range(num_epochs):
    for (words,labels) in train_loader:
        words= words.to(device)
        labels=labels.to(device).long()

        #Forward
        outputs= model(words)
        loss= criterion(outputs, labels)

        #Backward and Optimizer Step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


    if (epoch+1)%100==0:
        print(f'Epoch:{epoch+1}/{num_epochs}, Loss:{loss.item():.4f}')

print(f'Final Loss:{loss.item():.4f}')

data= {
    'model_state': model.state_dict(),
    'input_size': input_size,
    'output_size': output_size,
    'hidden_size': hidden_size,
    'all_words': all_words,
    'tags': tags
}

FILE='data.pth'
torch.save(data,FILE)

print(f'Training is Done and the file is saved to {FILE}')
