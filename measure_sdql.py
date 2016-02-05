from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
from string import Template
import os

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/J-2014.09-SP1/amd64/stildpv/"

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15"]:
        return "CLOCK"
    else:
        return "clock"

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

    settings['stil'] = target + '.proposexoptimise.stil'
    num = SortMinTransition.pattern_num(settings['stil'])
    for i in range(num):
        settings['last_p'] = i + 1
        os.system('echo ' + str(settings['last_p']) + ' >> ' + settings['stil'] + '.sdql')
        Synopsys.system(shell='tmax', script='../template/RequestSDQL_with_p', context=settings)
