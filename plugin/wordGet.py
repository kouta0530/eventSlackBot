# -*- coding: utf-8 -*
from janome.tokenizer import Tokenizer

def mecab(text):
    t = Tokenizer(wakati = True)
    malist = t.tokenize(text,wakati= True,stream = True)
    malist = ",".join(malist)
    
    return malist
