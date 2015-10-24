Dazai app
====

## How to use

config.yml
{  
  "booktitle": "実践　太宰治",
  "aut": "文學ラボ"
  "prt": "株式会社ポプルス"
  "pbl": "文學ラボ"
  "contact": "soycurd1@gmail.com"
  "prt_url":  "http://soy-curd.hatenablog.com/"
  "rights": "(C) 2015 @bungaku, lab"
}


## gunicorn
```
gunicorn app:app -b localhost:8002 -t 120
```
+ 再起動
```
pkill -HUP gunicorn
```
+ 殺す
```
pkill gunicorn
```
