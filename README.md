## 本フォルダについて

本フォルダは、書籍「現場で使える！Python深層強化学習入門」で解説されているコンテンツのソースコードを収めたものです。

## ファイル構成

本フォルダのファイル構成は以下のようになります。

```
RL_Book/
├── contents　#各章のサンプルプログラム（Python）
│    ├── 2_dp_officeworker  #第2章　会社員のMDP
│    ├── 3_keras_example    #第3章　MLP, CNN, RNN, LSTMのKeras実装
│    ├── 4-2_dqn_pendulum   #第4章　DQNによる倒立振子制御
│    ├── 4-3_ac_pendulum    #第4章　Actor-Critic法による倒立振子制御
│    ├── 5_walker2d         #第5章　ヒューマノイドの2足歩行
│    ├── 6-2_tsp            #第6章　巡回セールスマン問題
│    ├── 6-3_rubiks_cube    #第6章　ルービックキューブ解法
│    ├── 7-1_seqgan         #第7章　文書生成
│    └── 7-2_enas           #第7章　ニューラルアーキテクチャ探索
├── docker　#Docker環境構築用の設定ファイル
│    ├── Dockerfile
│    └── requirements.txt
├── README.md　
├── run_docker.sh　#Docker環境を起動する実行ファイル
└── demo.ipynb	#Docker環境でサンプルを実行するノートブック
```

#### ■ contents
書籍の各章・各節にて紹介したサンプルコードが、章ごと節ごとにフォルダに収められています。本フォルダをルートとしてコマンドラインで実行することを想定してます。

#### ■ docker

Windows PC上に開発環境を構築するためのDockerファイルと必要なPythonライブラリのリストを収めています。

#### ■ run_docker.sh

上記のDockerファイルから作成されたDockerイメージをもとに、コンテナ環境を起動するシェルスクリプトです。

#### ■ demo.ipynb

上記のシェルスクリプトを実行して起動されたコンテナ環境で、サンプルコードを実行するjupyterノートブックです。

## コーディング規則

- PEP8準拠
- flake8適用

## その他

利用法の詳細については、書籍の付録「開発環境の構築」を参照してください。

