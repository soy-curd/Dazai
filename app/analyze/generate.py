#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys

def main():
    
    # 『人間失格』のテキストデータを取得
    with open("ningen.txt", "r") as f:
        text = f.read()

    # 単語を分かち書き
    wordlist = wakati(text)
    print(wordlist)    
    
    # 『人間失格』バイグラムを作成
    bigram = make_bigram(wordlist)

    txt = ""
    while True:
        sys.stdout.write(">>" + txt)
        
        # 入力
        inp = input()
        if inp == 'q':
            break

        # テキストを更新
        txt = txt + inp
        
        # 最後の単語を取得
        last_word = wakati(txt)[-1]

        # バイグラムからデータを取得
        print(set(bigram.get(last_word, "")))
    
def make_bigram(wordlist):
    bigram = {}
    key = wordlist[0]
    for word in wordlist[1:]:
        # keyがbigramに存在しない場合、
        # 辞書にkeyを追加
        if key not in bigram:
            bigram[key] = [word]
        else:
            bigram[key].append(word)
        
        # keyを更新
        key = word
        
    return bigram

def wakati(text):
    import igo
    t = igo.Tagger.Tagger('ipadic')

    return t.wakati(text)

def print_json(bigram):
    import json
    text = json.dumps(bigram, ensure_ascii=False)
    print(text)

if __name__ == '__main__':
    main()
