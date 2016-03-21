from lib.sort_min_transition import SortMinTransition
from lib.verilog import Verilog
from lib.synopsys import Synopsys
import os
import subprocess
import time
import re
import shutil

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15"]:
        return "CLOCK"
    else:
        return "clock"


if __name__ == '__main__':
    # 実際に動かす
    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    target = 'b05'
    try:
        os.mkdir(target)
    except:
        pass;

    # ファイルを読み込む
    os.chdir(target)
    files = os.listdir('.')

    start_pattern_list = []
    end_pattern_list = []
    for i in range(1, int(len(files)/2) + 1):
        start_f = str(i) + '_start_' + target + '_comb.stil'
        end_f   = str(i) + '_end_' + target + '_comb.stil'
        start_pattern_list.append(SortMinTransition.extract_pattern_comb(start_f)[0])
        end_pattern_list.append(SortMinTransition.extract_pattern_comb(end_f)[0])
    os.chdir('..')
    output_l = SortMinTransition.make_initial_comb(target + '_base.stil')
    output_l.extend(SortMinTransition.pattern_to_file_comb(start_pattern_list))
    output_l.extend(SortMinTransition.make_after_comb(target + '_base.stil'))

    output_f = target + '_comb_start.stil'
    with open(output_f, 'w') as f:
        for i in output_l:
            f.write(i)

    output_l = SortMinTransition.make_initial_comb(target + '_base.stil')
    output_l.extend(SortMinTransition.pattern_to_file_comb(end_pattern_list))
    output_l.extend(SortMinTransition.make_after_comb(target + '_base.stil'))

    output_f = target + '_comb_end.stil'
    with open(output_f, 'w') as f:
        for i in output_l:
            f.write(i)
