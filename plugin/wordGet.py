# -*- coding: utf-8 -*-
def mecab():
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    malist = t.tokenize("今日の天気は晴れです",wakati= True)
    
    return malist
