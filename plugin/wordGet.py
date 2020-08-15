# -*- coding: utf-8 -*-
from janome.tokenizer import Tokenizer

def mecab():
    t = Tokenizer()
    malist = t.tokenize("今日の天気は晴れです")
    
    word = [n.surface for n in malist]

    return word
