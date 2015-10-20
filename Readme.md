Tips
======

ローカルの編集をサーバ上に反映させる
-----------------------------------
- rsyncを使う
 - 参考:[rsync - 高速なファイル同期（バックアップ） - Linuxコマンド](http://webkaru.net/linux/rsync-command/)
```
$ rsync -ruz --delete [コピー元] [コピー先]
$ rsync -ruz --delete . matsumoto@palau:/home/lab/matsumoto/Git/NNCT
```
