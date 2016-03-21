How to This
-----------
Python3で書かれています．
```
from lib.synopsys import Synopsys
```
と書くことで，lib/synopsys.py内のSynopsysクラスをインポートする
以下の記述はすべて，Synopsysクラスをインポートしたうえで行っている.

main.py の使い方
---------------
#### アプリケーションの実行
```
Synopsys.system(shell='dc', script='file_name')    # file内のコマンド通りにdc_shellの実行
Synopsys.system(shell='pt', script='file_name')    # file内のコマンド通りにpt_shellの実行
Synopsys.system(shell='tmax', script='file_name')  # file内のコマンド通りにtmaxの実行
```

#### templateファイル
コマンドをいちいち記述するのは手間なので，templateディレクトリ以下にtemplateファイルを置いている
templateファイルは，Python3のTemplateモジュールを使っており，$xyzの部分に値を代入できる

Synopsys.systemの引数のcontextにdict変数を渡すとtemplateファイル内に，dict変数の値を代入した結果を返してくれる

例: b03を論理合成する
```
target = 'b03'
settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
                    nangate_v  = '../data/Nangate/nangate.v',
                    name       = target,
                    clock      = clock_judge(target),
                    vhd        = '../data/Iscas99/' + target + '.vhd',
                    vg         = target + '.vg',
                    spf        = target + '.spf',
                    stil       = target + '.stil',
                    slk        = target + '.slk',
                    stilcsv    = target + '.stilcsv',
                    vcd        = target + '.vcd',
                    fault      = target + '_report_faults.txt',
                    power      = target + '_report_power',
                    first_p    = 1,
                    last_p     = 1
                    )

Synopsys.system(shell='dc', script='../template/LogicSynthesis', context=settings)  # LogicSynthesis内の`$hoge`の部分にsettings内のsettings['hoge']の値がが代入される
```

#### SDQLを求める
```
Synopsys.system(shell='dc', script='../template/LogicSynthesis', context=settings)
Synopsys.system(shell='pt', script='../template/AnalysisPass', context=settings)
Synopsys.system(shell='tmax', script='../template/GeneratePatternForSDQL', context=settings)
Synopsys.system(shell='tmax', script='../template/RequestSDQL', context=settings)
```

---
実験手順
--------
X 割り当て手法
1. main.pyを動かし，テストパターンを生成する 
2. make_comb_stil.py を動かし，baseファイルを作成する
3. test_si_x_fill.py を動かし，STIL上に存在するtest_siをX-Fillする 
4. generate_stil_from_test_si.py を実行し，STILファイルを作成する 
5. optimize.py を実行し，つくったSTILファイル内にあるXを割り当てる 
6. measure_power.py を実行し，電力を測定する 
7. measure_sdql.py を実行し，sdqlの遷移を測定する 
8. make_comb_test_stil.py を動かし組合せ回路のテストパターンを作る
9. measure_power_comb.py を動かし，組合せ回路に対する電力を求める
8. 組合せ回路に対してテストパターンを生成する 
9. 組み合わせ回路に対しbaseのstilファイルを作る

---
並び替え
--------
lib/sort_min_transition.py に並び替えのプログラムを記述している．
使い方については，githubのwikiを見よう
- sort_min_transitionは，ブロードサイド方式で作成したテストパターンにのみ有効であある
- `from lib.sort_min_transition import SortMinTransition` でimportする

---
電力の測定方法
--------------
電力測定関連のファイル・関数
- b0*.vg 
- b0*_stildpv.v (論理合成時に作成される)
- b0*_vcs.sh    (同上)
- b0*.vcd       (b0*_vcs.sh を動かすことで作成される)

電力想定の流れ
- STILDPV_HOMEを設定
- b0*_stildpv.v にコマンドを追加
- b0*_vcs.sh コマンドを実行
- PrimeTimeを実行

実際の例
- STILDPV_HOMEを設定
```
$ export STILDPV_HOME=/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv/ 
```

- b0*_stildpv.v にコマンドを追加
```
$ vim b0_stildpv.v
// initial begin以下に下の記述を追加
$dumpfile("b0?.vcd");
$dumpvars(0, b0?); 
```

- b0*_vcs.sh コマンドを実行
```
$ sh b0_vcs.sh //.vcdファイルが作成される
```

- PrimeTimeを実行

コマンドは，template/AnalysisPowerを参考に  
ちなみに，main.pyの中のanalysis_power()は，この作業を自動化している

