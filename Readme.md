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
