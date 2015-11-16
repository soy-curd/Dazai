太宰治小説の可視化
====

//lead{

読書という行為を、時間を抜きにして語ることはできない。例えば20000字程度の短編小説ならば、仮に分速500文字で読書可能だとすると、40分もの時間をわたしたちはそのテキストと向かい合うこととなる。わたしたちは読書を行っているあいだ、細胞の中でDNAを解読するリボソームのように、テキストをシリアルに視野から取り込み、脳の中で解釈していく。この際、解釈の方向は定められている。縦書きであれば上から下に。横書きであれば、（大抵の言語は）左から右に読まれるしかない。テキストは、ごく一部の例外を除けば、一方向にしか読まれ得ない。その点で、読書は非常に"時間"に似通った、あるいは随伴した現象だと考えられる。以前発行した同人誌『実用　どんぐりと山猫』では、pythonとd3.jsを用いて小説中のある値の時間変化を可視化した。昨今、可視化ツールとして、プログラミング不要な**Kibana**が開発されている。そこで本稿では、小説における時の流れをKibanaを用いて可視化し、より簡便な小説のテキストの解析を目指す。

//}




## 小説の中の時間構造

小説の中から、客観的な時間の指標を見出すことはできるだろうか。カフカ『城』に流れる停滞した時間。ボルヘス『バベルの図書館』における永遠の提示。桜庭一樹『私の男』で描写される逆行する日々。それら物語によって示される時間について、データとして評価できる形で客観的に抽出することは難しいだろう。そこで本稿では、小説の文字数を時間の指標とし、そこから見えてくる特徴を探していくこととする。

時間を軸としてある値を評価するためには、なんらかの基準が必要だ。一般には**タイムスタンプ**と呼ばれるものが用いられるが、小説には通常、そのような明確な時間の単位はない。今回はひとまず、これを500文字区切りで1づつ増える値と仮に設定する（文庫で1ページ程度に該当すると思われる）。そして可視化への中間地点として、以下のようなJSONデータを作成していく。


```JSON
[
  { 'page':1,
    'text':'春はあけぼの、やうやう白くなりゆく、山ぎは...'
  },
  { 'page':2,
    'text':'夏は夜。月のころはさらなり...'
  },
]
```


## 解析環境の用意


まずは自分のPCにpython3、Elasticsearch、Kibanaをインストールする。インストール法についての詳細は記述しない。また、解析するテキストについては、インターネット上に青空文庫や小説家になろうといった膨大なテキストデータがあるため、そちらを利用するのが早い。本稿では例として、太宰治『人間失格』のテキストを解析していくこととする。

## Elasticsearch

ElasticsearchはJava製の全文検索エンジンであり、Apach Solrと並んで人気が非常に高い。導入にあたっては、[^1]Wantedlyのエンジニアブログの内容がわかりやすいと思われる。今回重要な点としては、形態素解析器である**kuromoji**のプラグインを導入しておくことだ。

[^1]:  (http://engineer.wantedly.com/2014/02/25/elasticsearch-at-wantedly-1.html)

Elasticsearchにデータをインポートするにあたって、あらかじめデータのマッピング（どのデータがどんな種類のデータか指定すること）を行う必要がある。マッピングについては、以下の内容のanalyze.jsonを作成すると良い。

```
{
  "settings": {
    "analysis": {
      "filter": {
        "pos_filter": {
          "type": "kuromoji_part_of_speech",
          "stoptags": [
            "助詞-格助詞-一般",
            "助詞-終助詞"
          ]
        },
        "greek_lowercase_filter": {
          "type": "lowercase",
          "language": "greek"
        }
      },
      "tokenizer": {
        "kuromoji": {
          "type": "kuromoji_tokenizer"
        },
        "ngram_tokenizer": {
          "type": "nGram",
          "min_gram": "2",
          "max_gram": "3",
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      },
      "analyzer": {
        "kuromoji_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": [
            "kuromoji_baseform",
            "pos_filter",
            "greek_lowercase_filter",
            "cjk_width"
          ]
        },
        "ngram_analyzer": {
          "tokenizer": "ngram_tokenizer"
        }
      }
    }
  },
  "mappings": {
    "novel": {
      "_source": {
        "enabled": true
      },
      "_all": {
        "enabled": true,
        "analyzer": "kuromoji_analyzer"
      },
      "properties": {
        "id": {
          "type": "integer",
          "index": "not_analyzed"
        },
        "page": {
          "type": "integer",
          "index": "not_analyzed"
        },
        "text": {
          "type": "string",
          "index": "analyzed",
          "analyzer": "kuromoji_analyzer"
        }
      }
    }
  }
}

```

ここで、textフィールドにkuromoji_analyzerを指定している。こうすることで、解析テキストをあらかじめ形態素解析しておくことができる。


## 解析ファイルのJSON化

まず、『人間失格』のテキストデータを含んだningen.txtファイルを用意する。
そして、そのファイルを含んだディレクトリ上で、以下のpythonスクリプトを実行してみよう。

```python
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
        texts.append({ "index": { "_index": "dazai-demo",
                     "_type": "novel", "_id": x + 1 } })
        texts.append({'id':x + 1, 'text':text_of_page, 'page':x})
    
    bulk = ""
    for x in texts:
        bulk = bulk + json.dumps(x, ensure_ascii=False) + "\n"
    
    with open("./ningen.json", 'w') as f2:
        f2.write(bulk)
        
    print(bulk)

if __name__ == '__main__':
    main()

```

これを実行すると、カレントディレクトリ配下に以下のようなningen.json（正確には、JSONテキストを結合したもの）が生成される。

```
{"index": {"_type": "novel", "_id": 150, "_index": "dazai-demo"}}
{"page": 149, "text": "ュックサックを背負って友人の許もとを辞し、れいの喫茶店に立ち寄り、\n「きのうは、どうも。ところで、……」\n　（中略）もし、これが全部事実だったら、そうして僕がこのひとの友人だったら、やっぱり脳病院に連れて行きたくなったかも知れない」\n「", "id": 150}
```
これは、テキストを500字毎に区切り、（架空の）ページ番号を振ったものである。それでは、これらをElasticsearchにインポートしてみよう。

```
curl -XPUT localhost:9200/dazai-demo --data-binary @analyze.json
curl -XPOST localhost:9200/_bulk --data-binary @ningen.json 
```

その後、成功していたら以下のクエリによって検索が可能になっているはずである。

```
curl -XGET localhost:9200/dazai-demo/novel/_search -d '{"query":{"match":{"text":"東京"}}}'
```

問題なくデータのインポートは行えたであろうか。次項からは、Kibanaによる可視化を行っていく。


## Kibana

前項では、Elasticsearchへの小説データのインポートを行った。
それでは、それらのデータをデータ可視化ツールであるKibanaを用いて可視化していきたい。

まずは、https://www.elastic.co/downloads/kibanaからkibanaをダウンロードし（2015/11時点ではKibana 4.1.2）、展開したディレクトリ内の

```
bin/kibana
```
を実行してみよう。その後、ブラウザでhttp://localhost:5601にアクセスすると以下のような画面が表示される。

//image[001][Configure an Index pattern]{
//}


ここで、"Index name or pattern"に"dazai-demo"（indexの作成先）と入力して、Createを押下すると、インデックスがKibanaに登録される。

次に、Kibanaの左上に表示されている"Discover"を押下する。Elasticsearchへのデータのインポートに成功していれば、ここでデータを見ることができる。

例えば、"Selected Fields"にtextとpageを設定すると、以下のような画面となる。

//image[002][テキストの表示]{
//}

## ビジュアライズ

まずは、今回用いたテキスト『人間失格』の、頻出単語をヒストグラムにしてみよう。

Kibanaの画面から"Visualize"を押下すると、


//image[003][可視化方法の選定]{
//}


のように、可視化方法を選ぶ画面に遷移する。ここで、"Vertical bar chat" → "From a new search"と進んでいくと、ヒストグラムの要素を設定する画面に遷移する。

ここで、Y軸を単語数、X軸を各単語（頻度順）で表現したいとする。
これを行うのは非常に簡単だ。
まず、Y-AxisをCountに設定する。その後、buckets → X-Axisから

| ラベル | 設定内容|
|--------------------|--------------------|
| Aggregation | Terms|
| Field       | text |
| Order       | Top  |
| Size        | 60   |
| Order By    | metric: Count|

と設定する。

その後、左上にある右向きの三角形（再生ボタンに似ている）を押下してほしい。以下のような画像が表示されるはずだ。

//image[004][単語の頻度グラフ]{
//}

画像が表示されたら、右上の"Save Visualization"から、このグラフを保存しておこう。

それでは、グラフを見て欲しい。"た"、"だ"、"て"のような単語に紛れて、一番右に"人間"という単語がリストに（恣意的に！）含まれている。これは本文では、『もはや、自分は、完全に、人間で無くなりました』や、『自分には、淫売婦というものが、人間でも、女性でもない、白痴か狂人のように見え、そのふところの中で、自分はかえって全く安心して、ぐっすり眠る事が出来ました。』といった描写に用いられる、非常に重要な単語である。

それでは、次の章ではこの『人間失格』という小説の中で、"人間"という単語がいつ、どの程度用いられるかを可視化する。

## 小説内における単語の頻度推移

それでは、ページ毎の"人間"という単語の頻度の推移を追ってみよう。

まずは先ほどの手順同様、新しく"Vertica Bar Chart"を作成してもらいたい。

前回、pythonによってページ毎にテキストを分割していた。今回のx軸はページ、y軸を"人間"の単語数とする。


今回もY-AxisをCountに設定し、buckets → X-Axisは

| ラベル | 設定内容|
|--------------------|--------------------|
| Aggregation | Histogram|
| Field       | page |
| Interval       | 5  |

と設定する。

そして、上部の検索窓に"人間"と入力して、グラフを生成して欲しい。下のようなグラフが生成されるはずだ。

//image[005][ページ毎の"人間"の推移]{
//}

検定は行わずに印象で判断すると、小説の後半数十ページ、"人間"という単語が使われる頻度が激減している箇所がある。これが、作中の主人公の人間性と関連していたら非常に面白いのだが、残念ながらそのような結論を導くにはもっと精緻な分析が必要であろう。しかし、このようなレベルの可視化でも、どのように太宰治の小説を読んでいくかのヒントの一つとすることはできるかもしれない。

## おわりに
以上、PythonとElasticsearch、Kibanaを用いて太宰治『人間失格』の可視化を行った。このような解析が、オープンソース（プログラムのソースコードが世界に公開されていること）のプログラムでできることは、非常に好ましいことである。小説に対する新しい切り口が欲しい、あるいは文系分野の定量化に興味のある方は、これを機にこれらのツールを利用してみることをお勧めしたい。(soy-curd)
