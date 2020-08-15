# -*- coding: utf-8 -*-
import MeCab

def mecab():
    mecab = MeCab.Tagger("")
    text = """今日の天気は晴れです．"""
    nouns = [line.split()[0] for line in mecab.parse(text).splitlines()
                if "名詞" in line.split()[-1]]
    return nouns