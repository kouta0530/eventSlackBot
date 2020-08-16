# -*- coding: utf-8 -*
from janome.tokenizer import Tokenizer

def mecab(text):
    t = Tokenizer()
    malist = t.tokenize(text,wakati= True)
    #malist = ",".join(malist)
    
    return malist
