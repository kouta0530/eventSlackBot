# -*- coding: utf-8 -*-

def mecab():
    """
    mecab = MeCab.Tagger()
    text = 今日の天気は晴れです．
    nouns = [line.split()[0] for line in mecab.parse(text).splitlines()if "名詞" in line.split()[-1]]
    return text
    """

    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    malist = t.tokenize("今日の天気は晴れです")
    
    word = [n.surface for n in malist]

    return word
