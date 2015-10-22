from lib.synopsys import Synopsys
from string import Template
import os


if __name__ == '__main__':
    target = 'b03'
    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
                    nangate_v = '../data/Nangate/nangate.v',
                    name = target,
                    vhd = '../data/Iscas99/' + target + '.vhd',
                    vg = '../data/Output/' + target + '.vg',
                    spf = '../data/Output/' + target + '.spf',
                    stil = '../data/Output/' + target + '.stil',
                    slk = '../data/Output/' + target + '.slk',
                    stilcsv = '../data/Output/' + target + '.stilcsv',
                    fault = '../data/Output/' + target + '_report_faults.txt'
                    )

    ## 論理合成
    combine = Synopsys.combine('../template/LogicSynthesis', settings)
    Synopsys.dc_shell(combine)

    ## パス検出
    combine = Synopsys.combine('../template/AnalysisPass', settings)
    Synopsys.pt_shell(combine)

    ## テストパターン生成
    combine = Synopsys.combine('../template/GeneratePatternForSDQL', settings)
    Synopsys.tmax(combine)

    # SDQLを求める
    combine = Synopsys.combine('../template/RequestSDQL', settings)
    Synopsys.tmax(combine)

    # ローカルにファイル転送
    os.system('rsync -ruz ../. kazutaka@192.168.7.149:/Users/kazutaka/Git/NNCT_Sudy')


