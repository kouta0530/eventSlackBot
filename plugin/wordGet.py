# -*- coding: utf-8 -*
from janome.tokenizer import Tokenizer

def mecab(text):
    t = Tokenizer()
    malist = t.tokenize(text)

    words =  [i.surface for i in malist if i.part_of_speech.split(",")[0] == "名詞"]
    
    return words
