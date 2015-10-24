Dazai
====

同人誌『実践 太宰治』のリポジトリです。
pdfにコンパイルするためには、texとrubyが必要です。

## review install
```sh
# md2reviewのインストール
sudo gem install md2review

# reviewのインストール
# A5版のpdfを作成するため、A5版改造済reviewをgit cloneする。
git clone https://github.com/soy-curd/review.git
cd review
sudo rake install
cd ..
cd doc
md2review xxx.md > xxx.re
review-pdfmaker config.yml
```
