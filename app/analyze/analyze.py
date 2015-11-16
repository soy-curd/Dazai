#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def main():
    
    with open("./ningen.txt", "r") as f1:
        text = f1.read()
    
    # 1ページの文字数を500文字と仮定
    pseud_char_num_per_page = 500
    
    # ページ毎にテキストを区切っていく
    page_num = len(text) // pseud_char_num_per_page
    
    texts = []
    for x in range(page_num):
        init = x * pseud_char_num_per_page
        text_of_page = text[init: init + pseud_char_num_per_page]
        texts.append({ "index": { "_index": "dazai-demo", "_type": "novel", "_id": x + 1 } })
        texts.append({'id':x + 1, 'text':text_of_page, 'page':x})
    
    bulk = ""
    for x in texts:
        bulk = bulk + json.dumps(x, ensure_ascii=False) + "\n"
    
    with open("./ningen.json", 'w') as f2:
        f2.write(bulk)
        
    print(bulk)

if __name__ == '__main__':
    main()
