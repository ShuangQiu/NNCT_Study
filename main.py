from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
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

def make_dump(settings):
    ## stildpv.v ファイルにdumpファイルを生成するプログラムの追加
    already = False
    with open(settings["name"] + '_stildpv.v', 'r') as f:
        stil_file = f.readlines()
    for i in stil_file:
        if 'vector_number = 0;' in i:
            index = stil_file.index(i)
        if '$dumpfile(' in i:
            # すでにdumfileが書かれていた場合
            already = True
    if already != True:
        stil_file.insert(index+1, '$dumpfile("' + settings["name"] + '.vcd");\n')
        stil_file.insert(index+2, '$dumpvars(0, ' + settings["name"] + ');\n')
        with open(settings["name"] + '_stildpv.v', 'w') as f:
            f.writelines(stil_file)

def analysys_power(settings):
    ## 電力を求める
    # vcdファイルを作るためのshを実行
    make_dump(settings)
    os.system('bash ' + settings["name"] + '_vcs.sh')

    combine = Synopsys.combine('../template/AnalysisPower', settings)
    Synopsys.pt_shell(combine)

def analysys_power_f(settings, f):
    ## ファイル指定したstilで電力を求める
    os.system('cp ' + settings["stil"] + ' temp.stil')
    os.system('cp ' + f + ' ' + settings["stil"])

    settings["power"] = f + '_report_power.txt'

    make_dump(settings)
    os.system('bash ' + settings["name"] + '_vcs.sh')

    combine = Synopsys.combine('../template/AnalysisPower', settings)
    Synopsys.pt_shell(combine)

    os.system('cp ' + ' temp.stil ' + settings["stil"])
    os.remove('temp.stil')

def synth_to_SDQL(settings):
    logic_synthesis(settings)
    analysys_pass(settings)
    generate_pattern(settings)
    request_SDQL(settings)

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15"]:
        return "CLOCK"
    else:
        return "clock"


if __name__ == '__main__':
    target = 'b10'
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
                    vcd        = target + '.vcd',
                    fault      = target + '_report_faults.txt',
                    power      = target + '_report_power.txt'
                    )

    synth_to_SDQL(settings)
    analysys_power(settings)
    SortMinTransition.sort('b04.stil', 'b04_sort.stil')
    analysys_power_f(settings, 'b10_sorted.stil')

    # ローカルにファイル転送
    # os.system('rsync -ruz ../. kazutaka@192.168.7.149:/Users/kazutaka/Git/NNCT_Sudy')

