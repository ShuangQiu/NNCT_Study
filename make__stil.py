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
    target = 'b08'
    try:
        os.mkdir(target)
    except:
        pass;
    # vgファイルから組み合わせ回路を抜き出し，vgファイルに戻す
    Verilog.convert_verilog_to_json(target + '.vg', output_f= target + '.json')
    Verilog.extract_comb_circuit_from_verilog_json(target + '.json', target + '.json')
    Verilog.convert_json_to_verilog(target + '.json', output_f=target + '_comb.vg')
    # Test Pattern の 生成
    settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
            nangate_v  = '../data/Nangate/nangate.v',
            name       = target,
            clock      = clock_judge(target),
            vg         = target + '_comb.vg',
            stil       = target + '_base.stil',
            pi_constraints = '',
            fault_sentence = 'add_faults -all'
            )

    # テストパターン生成の実行
    Synopsys.run(shell='tmax', script='../template/GeneratePatternForCombination', context=settings)
