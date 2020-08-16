# SlaReco

「SlaReco」はSlack上にニュースをレコメンドしてくれるアプリケーションです．

![frontimage](https://github.com/kouta0530/eventSlackBot/blob/master/materials/demo5.png?raw=true)

## Introduction

就活をしていると企業の方や先生から言われます．  
「ニュースを見ろ」と．
しかし，朝から進んで探すのは面倒くさい．  
そこで思いました，朝一に閲覧する習慣のあるslackに自動でニュースがアップされたらいいなと．それがこのアプリを作成した切っ掛けです．

## Features

heroku上でpythonを使用しました．

![TechnologyStack](https://github.com/kouta0530/eventSlackBot/blob/master/materials/slide.png?raw=true)

### スクレイピング
ニュース記事を探してくる機能．ニュースはITメディアを採択．
### 共有
ブックマークした記事を共有する機能．
### レコメンド
ワークスペースで話題の記事を選んでくれる機能．

## Requirement

heroku環境を前提としています．
* heroku
* Python 3.6.5

以下requirements.txtより
* Flask 1.0.2
* slack 0.0.2
* slackeventsapi 2.2.1
* slackclient 2.8.0
* gunicorn 20.0.4
* bs4 0.0.1
* requests 2.23.0
* psycopg2 2.8.5

## Author
サマーハッカソン参加チーム：TDU
