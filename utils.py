import nltk
#nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
import numpy as np

def tokenize(sentence):  #This will get a Sentence as the Input
  return nltk.word_tokenize(sentence)

stemmer=PorterStemmer()
def stemming(word):  #This will get a word as the input
  return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
      """
      return bag of words array:
      1 for each known word that exists in the sentence, 0 otherwise
      example:
      sentence = ["hello", "how", "are", "you"]
      words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
      bag   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
      """
      # We will pass the all_words which are already stemmed

      tokenized_sentence= [stemming(w) for w in tokenized_sentence]
      bag= np.zeros(len(all_words), dtype=np.float32)  #[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
                                                         # 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
                                                         # 0. 0. 0. 0. 0. 0.]
      for idx, w in enumerate(all_words):
        if w in tokenized_sentence:  #If w is present in the tokenized sentence
          bag[idx]=1.0

      return bag

# a='How are you doing?'
# print(a)
# a=tokenize(a)
# print(a)

# a=['Swimming','boxing','Dancing']
# print(a)
# a= [stemming(i) for i in a]
# print(a)


# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bag= bag_of_words(sentence,words)
# print(bag)     #[0. 1. 0. 1. 0. 0. 0.]