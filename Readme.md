How to This
===========
Python3で書かれています．
```
from lib.synopsys import Synopsys
```
と書くことで，lib/synopsys.py内のSynopsysクラスをインポートする
以下の記述はすべて，Synopsysクラスをインポートしたうえで行っている.

アプリケーションの実行
--------------
```
Synopsys.dc_shell(file)  # file内のコマンド通りにdc_shellの実行
Synopsys.pt_shell(file)  # 同上
Synopsys.tmax(file)  # 同上
```

templateファイル
----------------
コマンドをいちいち記述するのは手間なので，templateディレクトリ以下にtemplateファイルを置いている
templateファイルは，Python3のTemplateモジュールを使っており，$xyzの部分に値を代入できる

tempファイルの作成・結合
--------------------
Synopsys.combineでは，引数の一つ目に，templateファイル，二つ目にdict変数を渡すことで，templateファイル内に，dict変数の値を代入した結果を返してくれる
```
settings = dict(nangate_db = 'data/Nangate/nangate45nm.db',
                    nangate_v = 'data/Nangate/nangate.v'
                    name = 'b03',
                    vhd = 'data/Iscas99/' + name + '.vhd',
                    vg = 'data/Output/' + name + '.vg',
                    spf = 'data/Output/' + name + '.spf',
                    stil = 'data/Output/' + name + '.stil',
                    slk = 'data/Output/' + name + '.slk',
                    stilcsv = 'data/Output/' + name + '.stilcsv'
                    fault = 'data/Output/' + name + '_report_faults.txt'
                    )

combine = Synopsys.combine('template/LogicSynthesis', settings)
```

Tips
======

ローカルの編集をサーバ上に反映させる
-----------------------------------
- rsyncを使う
 - [rsync - 高速なファイル同期（バックアップ） - Linuxコマンド](http://webkaru.net/linux/rsync-command/)
```
$ rsync -ruz --delete [コピー元] [コピー先]
$ rsync -ruz --delete . matsumoto@palau:/home/lab/matsumoto/Git/NNCT_Study --exclude .git/
```

リモート先からファイルを持ってくる
----------------------------------
```
$ scp -r matsumoto@palau:/home/lab/matsumoto/Study/Nangate .
$ rsync -ruz --delete matsumoto@palau:/home/lab/matsumoto/Git/NNCT_Study/. .
$ rsync -ruz --delete matsumoto@palau:/home/lab/matsumoto/Git/NNCT_Study/. . --exclude .git/
```

Q&A
===

Q. ATPGでつくったやつとSimlationでは，SDQL値が違うんですけどなぜですか?
--------------------------------------------------------------------
A. 上がAPTG生成時にSDQLを求めたもの，下がシミュレーションでSDQLを求めた時の故障の数です．
このように，ATPG生成時のDTとシミュレーション時のDTの数が異なっています．
この傾向は，遅延故障を考慮した部分を抜いた場合でも起こります．

ここから，ATPG生成時のもののdetectedの中でATPGでのみテスト可能なな故障がいくつか存在し，
それが，シミュレーション時にnot detectedになったと推論できる

```
 -----------------------------------------------
 fault class                     code   #faults
 ------------------------------  ----  ---------
 Detected                         DT       2167
 Possibly detected                PT          0
 Undetectable                     UD         80
 ATPG untestable                  AU        153
 Not detected                     ND        336
 -----------------------------------------------
 total faults                              2736
 test coverage                            81.59%
 -----------------------------------------------
            Pattern Summary Report
 -----------------------------------------------
 #internal patterns                         347
     #fast_sequential patterns              347
 -----------------------------------------------


 -----------------------------------------------
 fault class                     code   #faults
 ------------------------------  ----  ---------
 Detected                         DT       2159
 Possibly detected                PT          0
 Undetectable                     UD         80
 ATPG untestable                  AU          0
 Not detected                     ND        497
 -----------------------------------------------
 total faults                              2736
 test coverage                            81.29%
 fault coverage                           78.91%
 ATPG effectiveness                       81.83%
 -----------------------------------------------
            Pattern Summary Report
 -----------------------------------------------
 #internal patterns                           0
 #external patterns (../data/Output/b04.stil)    347
     #fast_sequential patterns              347
 -----------------------------------------------
```
