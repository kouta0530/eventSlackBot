import MeCab

# mecabでテキストを名詞だけ注した結果を返す
def mecab_keitaiso(text):
    mecab = MeCab.Tagger("-Ochasen")
    nouns = [line.split()[0] for line in mecab.parse(text).splitlines()
               if "名詞" in line.split()[-1]]
    return nouns

if __name__ == "__main__":
    text = "今日の天気は晴れです"
    print(mecab_keitaiso(text))