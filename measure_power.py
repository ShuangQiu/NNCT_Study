from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
from string import Template
import os
import subprocess

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/J-2014.09-SP1/amd64/stildpv/"

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

    settings["power"] = settings['name'] + '_report_power_sorted'

    make_dump(settings)
    os.system('bash ' + settings["name"] + '_vcs.sh')

    combine = Synopsys.combine('../template/AnalysisPower', settings)
    Synopsys.pt_shell(combine)

    os.system('cp ' + ' temp.stil ' + settings["stil"])
    os.remove('temp.stil')

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15"]:
        return "CLOCK"
    else:
        return "clock"

def get_sdql_with_p(settings):
    num = SortMinTransition.pattern_num(settings['stil'])
    for i in range(num):
        settings['last_p'] = i + 1
        request_SDQL_with_p(settings)

def all_circuits(settings):
    for t in ['b02', 'b03', 'b04', 'b05', 'b06', 'b07', 'b08', 'b09', 'b10', 'b11', 'b12', 'b13', 'b14', 'b15', 'b17','b18', 'b19', 'b20', 'b21', 'b22']:
        settings['target'] = t
        synth_to_SDQL(settings)

if __name__ == '__main__':
    target = 'b05'

    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    settings_path()

    settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
                    nangate_v  = '../data/Nangate/nangate.v',
                    name       = target,
                    clock      = clock_judge(target),
                    vhd        = '../data/ITC99/' + target + '.vhd',
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

    # 論理合成をしてSDQLをもとめる
    #Synopsys.system(shell='dc', script='../template/LogicSynthesis', context=settings)
    #Synopsys.system(shell='pt', script='../template/AnalysisPass', context=settings)
    #Synopsys.system(shell='tmax', script='../template/GeneratePatternForSDQLwithX', context=settings)
    #Synopsys.system(shell='tmax', script='../template/RequestSDQL', context=settings)

    # 電力をもとめる
    Synopsys.add_dump_code_in_stildpv(circuit='b05')

    Synopsys.compute_test_power(context=settings,stil_f=target + '.xoptimise.stil')
    Synopsys.compute_test_power(context=settings,stil_f=target + '.proposexoptimise.stil')
    Synopsys.compute_test_power(context=settings,stil_f=target + '.randomoptimise.stil')


