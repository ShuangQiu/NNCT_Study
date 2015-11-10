from lib.synopsys import Synopsys
from string import Template
import os

def logic_synthesis(settings):
    ## 論理合成
    combine = Synopsys.combine('../template/LogicSynthesis', settings)
    Synopsys.dc_shell(combine)

def analysys_pass(settings):
    ## パス検出
    combine = Synopsys.combine('../template/AnalysisPass', settings)
    Synopsys.pt_shell(combine)

def generate_pattern(settings):
    ## テストパターン生成
    combine = Synopsys.combine('../template/GeneratePatternForSDQL', settings)
    Synopsys.tmax(combine)

def request_SDQL(settings):
    ## SDQLを求める
    combine = Synopsys.combine('../template/RequestSDQL', settings)
    Synopsys.tmax(combine)

#def analysys_power(settings):
#    ## 電力を求める
#    combine = Synopsys.combine('../template/AnalysisPower', settings)
#    Synopsys.pt_shell(combine)

def SynthToSDQL(settings):
    logic_synthesis(settings)
    analysys_pass(settings)
    generate_pattern(settings)
    #request_SDQL(settings)

def clockJudge(target):
    if target in ["b04", "b05", "b08", "b15", "b17"]:
        return "CLOCK"
    else:
        return "clock"

if __name__ == '__main__':
    target = 'b04'
    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更

    settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
                    nangate_v = '../data/Nangate/nangate.v',
                    name = target,
                    clock = clockJudge(target),
                    vhd = '../data/Iscas99/' + target + '.vhd',
                    vg = '../data/Output/' + target + '.vg',
                    spf = '../data/Output/' + target + '.spf',
                    stil = '../data/Output/' + target + '.stil',
                    slk = '../data/Output/' + target + '.slk',
                    stilcsv = '../data/Output/' + target + '.stilcsv',
                    fault = '../data/Output/' + target + '_report_faults.txt'
                    )


    SynthToSDQL(settings)
    #analysys_power(settings)

    # ローカルにファイル転送
    # os.system('rsync -ruz ../. kazutaka@192.168.7.149:/Users/kazutaka/Git/NNCT_Sudy')

