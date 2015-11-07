太宰治小説の単語バイグラムを用いた執筆補助プログラムの作成
====

//lead{

前章では太宰治『人間失格』のテキストに用いられている単語を抽出し、可視化を行った。これで、太宰治の小説構造への理解が、多少なりとも深まったかもしれない。ここでもし、あなたが創作に興味を少しでも持っているならば、「太宰治のような小説を書くにはどうすれば良いだろう？」と思うこともあるだろう。そこで本章では、太宰治のテキストを利用し、太宰治の小説に含まれる単語をサジェストする、小説の執筆補助プログラムを作成していく。

//}

## 概要

例えばここに、『今日私はラーメンを食べた』という文章があったとする。この文章を単語毎に、「今日」「私」「は」「ラーメン」「を」「食べた」と分割する。この時、これらの単語をランダムに並べ替え、「は」「私」「今日」「食べた」「を」「ラーメン」とすると、日本語としておかしい文章になってしまう。ある日本語の文を生成するためには、単語を適切な順番で並べる必要がある。それでは、プログラミングによって正しい語順を得るにはどうすれば良いのだろうか。可能であるならば、日本語の文法規則を網羅した「日本語の文法に従って文章を組み立てるプログラム」を作成したいところだが、それには、文法規則を自分たちで学び、プログラムに落としこむ手間がかかる。しかし、そんなことをせずとも、すでに存在する文章を用いることによって、簡単に比較的日本語らしい文章を生成することができる。

例えば、「私」という単語があったとき、次に結合する単語としては、「は」「が」「を」などの助詞が想定されるだろう。もちろんこれらの「私は」「私が」などの繋がりは、日本語の規則に従っているものであると同時に、実際に一般的な日本語の文章の中で用いられているものでもある。つまり、ある日本語データの中から、「私」とその後に続く単語のリストを抽出すれば、「私」の後に接続しやすい単語を得ることができる。あとはこのリストを用いて、ある入力された言葉から、先に続くことばを推定し、利用者に対して表示するプログラムを作成すれば良い。

それではどのようにすれば、適切な単語のリストを作成することができるのだろうか。
例えば、「太宰治の小説」と「Amazonの口コミデータ」をひとつずつピックアップした際、どちらが「太宰治の小説」でどちらが「Amazonの口コミデータ」か判別することは、大抵の人には容易なことだろう。このような分類が行えることの非常に単純な仮設として、「太宰治の小説」と「Amazonの口コミデータ」では、用いられている単語の種類が異なることが考えられる。逆に考えると、「太宰治の小説」で用いられている単語を用いることで、太宰治の小説らしい文章が作成できる可能性がある。

例えば、太宰治の作品から単語のリストを得た際、それらを用いたプログラムにおいて期待される入力と出力は、

```
input 「人間」
output 「失格」

input 「ヴィヨン」
output 「と」

input 「ヴィヨンと」
output 「妻」
```

というようなものであるということにする。これらの入力と出力の組合せは、意味の成立している文章を作成する用途にはいささか心もとないが、執筆が暗礁に乗り上げた際のひとつのサジェスチョンとしては、効果のあるものになる可能性がある。それでは以下、実際に以上のような機能を実現するプログラムを作成する。


## 実装

プログラミングには、python3.4.3を用いる。それではまず、以下のように、文章を各単語に分解したリストを用意する。

```
wordlist = ['たとえば', '、', '私', 'が', 'この', '写真', 'を', '見', 'て', '、', '眼', 'を', 'つぶる', '。', '既に', '私', 'は', 'この', '顔', 'を', '忘れ', 'て', 'いる', '。']
```

そして、辞書オブジェクトを用意し、
{単語：[単語の次の単語]}となるように値を代入していく。ここで、ある単語によって取得される値は、リストになることに注意してほしい。つまり、上のような文字列に対しては、{"私": ["が", "は"]}という、2つの値を含んだリストが最終的に得られる必要がある。

この処理を実現したのが以下のプログラムだ。


```python

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

wordlist = ['たとえば', '、', '私', 'が', 'この', '写真', 'を', '見', 'て', '、', '眼', 'を', 'つぶる', '。', '既に', '私', 'は', 'この', '顔', 'を', '忘れ', 'て', 'いる', '。']

make_bigram(wordlist)

```

これによって作成されるデータは、以下となる。

```
{"つぶる": ["。"], "いる": ["。"], "が": ["この"], "この": ["写真", "顔"], "忘れ": ["て"], "たとえば": ["、"], "て": ["、", "いる"], "私": ["が", "は"], "見": ["て"], "写真": ["を"], "顔": ["を"], "を": ["見", "つぶる", "忘れ"], "は": ["この"], "、": ["私", "眼"], "。": ["既に"], "眼": ["を"], "既に": ["私"]}
```

これは、**単語バイグラム**と呼ばれる構造だ。例えばこの辞書に、"私"と入力すると、"私"に続く全ての単語を含んだリストが取得できる。それでは、『人間失格』の単語バイグラムを作成してみよう。

まずは以下のように、igo-pythonという形態素解析ライブラリを用いてテキストデータの分かち書きを行う。
```python
def wakati(text):
    """
    "私は" -> ["私", "は"]というように
    分かち書きされる。
    
    別途ipa辞書のインストールが必要なため注意。
    """
    
    import igo
    t = igo.Tagger.Tagger('ipadic')

    return t.wakati(text)
```
あとは、入出力部分を作成するだけだ。


```python
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
```

それでは、実際にこのプログラムを動かしてみよう。


## デモ
例えば以下のような文章を作成している途中、次に記述するべき単語がどうしても思い浮かばなかったとする。

```
今日は良い天気だ。私は
```

先ほど作成したプログラム上で、先ほどの文章を入力してみる。すると、

```
{'油絵', '実に', '思っ', 'いちど', '無い', 'いっ', '思い出す', '雪', '持ち前', '竹', '使っ', '黙っ', '薄れ', '過失', '眼', ----（中略）----, '理解'}

```

出力として、”は"という単語の後に『人間失格』内で用いられている単語がリストアップされる。
試しに、リストアップされた単語の最初のものだけを選択し、入出力を行っていく。

```
今日は良い天気だ。私は油絵の予言を警戒し強烈に
```

生成された単語の前後の繋がりが、日本語として適切であることが確認できるだろう。文章のヒントが得られたら、その後は自分で執筆を続けてみよう。もしかしたら過去の文豪に匹敵する文章が完成するかもしれない。

以上のように文章作成の際にプログラムを用いることで、執筆の際のアイディア源を増やすことができる可能性がある。創作に詰まってしまった方は、ぜひ以上のような方法を試し、新たなる創作の糧としていただきたい。