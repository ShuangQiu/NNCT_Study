from lib.synopsys import Synopsys
from string import Template
import os

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv/"

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

def analysys_power(settings):
    ## 電力を求める
    os.system('bash ' + settings["name"] + '_vcs.sh')

    ## stildpv.v ファイルにdumpファイルを生成するプログラムの追加
    combine = Synopsys.combine('../template/AnalysisPower', settings)
    Synopsys.pt_shell(combine)

def synth_to_SDQL(settings):
    logic_synthesis(settings)
    analysys_pass(settings)
    generate_pattern(settings)
    request_SDQL(settings)

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15", "b17"]:
        return "CLOCK"
    else:
        return "clock"

if __name__ == '__main__':
    target = 'b04'
    settings_path()
    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    #os.chdir('data/Output')  # よくわからないファイルが出るので作業ディレクトリの変更

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
                    fault      = target + '_report_faults.txt'
                    )


    #synth_to_SDQL(settings)
    analysys_power(settings)

    # ローカルにファイル転送
    # os.system('rsync -ruz ../. kazutaka@192.168.7.149:/Users/kazutaka/Git/NNCT_Sudy')

