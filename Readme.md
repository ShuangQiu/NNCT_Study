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
$ rsync -ruz --delete . matsumoto@palau:/home/lab/matsumoto/Git/NNCT_Study
```

リモート先からファイルを持ってくる
----------------------------------
```
$ scp -r matsumoto@palau:/home/lab/matsumoto/Study/Nangate .
```

