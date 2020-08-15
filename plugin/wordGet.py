# -*- coding: utf-8 -*-
def mecab():
    from janome.tokenizer import Tokenizer
    t = Tokenizer(wakati = True)
    malist = t.tokenize("今日の天気は晴れです",wakati= True,stream = True)
    malist = ",".join(malist)
    
    return malist
