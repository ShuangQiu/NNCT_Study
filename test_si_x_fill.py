from lib.sort_min_transition import SortMinTransition
from lib.verilog import Verilog
from lib.synopsys import Synopsys
import os
import subprocess
import time
import re

def clock_judge(target):
    if target in ["b04", "b05", "b08", "b15"]:
        return "CLOCK"
    else:
        return "clock"


if __name__ == '__main__':
    # 実際に動かす
    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    target = 'b05'
    # vgファイルから組み合わせ回路を抜き出し，vgファイルに戻す
    Verilog.convert_verilog_to_json(target + '.vg', output_f= target + '.json')
    Verilog.extract_comb_circuit_from_verilog_json(target + '.json', target + '.json')
    Verilog.convert_json_to_verilog(target + '.json', output_f=target + '_comb.vg')

    # 開始するパターン数の指定
    start_pattern = 0

    pattern_num = 0
    # scan_inの抽出
    for pattern in SortMinTransition.extract_pattern(target + '.stil'):
        already_fault_stuck = []
        script = []
        pattern_num += 1
        if pattern_num < start_pattern:
            continue
        input_pattern = pattern['test_si'].replace('N', 'x')
        try:
            os.remove(target + '_comb.stil')
        except:
            pass
        try:
            os.remove(target + '_test.v')
        except:
            pass

        os.system("pkill -f 'tmax*'")
        while True:
            print('-------------------------')
            print('input :' + input_pattern)
            script.append("ppi_ps_reg = " + str(len(input_pattern)) + "'b" +input_pattern + ';')
            script.append('$monitor("%b", ppo_ps_reg);')
            script.append('#100 $finish;')
            Verilog.convert_json_test_bench(target + '.json', script_l=script, output_f=target + '_test.v')
            script = []

            # vcs の 実行
            STILDPV_HOME = "/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv"
            DPV_FILE = target + '_test.v'
            NETLIST_FILES = target + '_comb.vg'
            LIB_FILES = '-v ../data/Nangate/nangate.v'
            output = subprocess.check_output('vcs -R +acc+2 -P ' + STILDPV_HOME + '/lib/stildpv_vcs.tab +tetramax +delay_mode_zero ' \
                    + DPV_FILE + ' ' + NETLIST_FILES + ' '  + LIB_FILES + ' ' + STILDPV_HOME + '/lib/libstildpv.a', shell=True)
            #output = os.system('vcs -R +acc+2 -P ' + STILDPV_HOME + '/lib/stildpv_vcs.tab +tetramax +delay_mode_zero ' \
            #        + DPV_FILE + ' ' + NETLIST_FILES + ' '  + LIB_FILES + ' ' + STILDPV_HOME + '/lib/libstildpv.a')
            output_pattern = re.search('[x01]{' + str(len(pattern['test_si'])) + '}', str(output)).group(0)

            print('output:' + output_pattern)

            # 入力の制約付きのPINを求める
            constraints_pin_dict = {}
            pin_num = 0
            for i_p, o_p in zip(input_pattern, output_pattern):
                # if i_p == 'x' and o_p == 'x':
                # if i_p == 'x' and o_p != 'x': 両方パス
                # 制約でi_pをo_pの値にしてもいいがそれによって出力が変わる可能性があるのでpass
                if i_p != 'x' and o_p == 'x':
                    constraints_pin_dict[pin_num] = i_p;
                elif i_p != 'x' and o_p != 'x':
                    constraints_pin_dict[pin_num] = i_p;
                pin_num += 1
            pi_constraints = ''
            for pin_num, pin_value in constraints_pin_dict.items():
                pi_constraints += 'add_pi_constraints ' + pin_value + ' ppi_ps_reg[' + str(pin_num) + ']\n'
            #print(pi_constraints)

            # 故障の設定
            # 問題点，最初の入力が優先されてしまうため，無限ループに陥る
            pin_num = 0
            fault_sentence = ''
            for i_p, o_p in zip(input_pattern, output_pattern):
                if i_p != 'x' and o_p == 'x':
                    if not pin_num in already_fault_stuck:
                        # stuck の 判定
                        if i_p == '1':
                            stuck = '0'
                        elif i_p == '0':
                            stuck = '1'
                        fault_sentence = 'add_faults ppo_ps_reg[' + str(len(input_pattern) - pin_num -1 ) + '] -stuck ' + stuck
                        already_fault_stuck.append(pin_num)
                        break
                pin_num += 1
            #fault_sentence = 'add_faults ppo_ps_reg[11] -stuck 1'
            print('fault :' + fault_sentence)

            # ループの終了
            if len(fault_sentence) == 0 :
                with open(target + '.test_si', 'a+') as f:
                    f.write(str(pattern_num) + ' ' + input_pattern + '\n')
                print('pattern finish')
                break

            # Test Pattern の 生成
            settings = dict(nangate_db = '../data/Nangate/nangate45nm.db',
                        nangate_v  = '../data/Nangate/nangate.v',
                        name       = target,
                        clock      = clock_judge(target),
                        vg         = target + '_comb.vg',
                        stil       = target + '_comb.stil',
                        pi_constraints = pi_constraints,
                        fault_sentence = fault_sentence
                        )
            Synopsys.run(shell='tmax', script='../template/GeneratePatternForCombination', context=settings)

            # 生成されたテストパターンの取得
            try:
                next_input_pattern = SortMinTransition.extract_pattern_comb(target + '_comb.stil')[0]['pi']
            except:
                print('パターンが見つかりませんでした')
                continue
            next_input_pattern = list(next_input_pattern)
            #next_input_pattern.reverse()
            next_input_pattern = ''.join(next_input_pattern)
            next_input_pattern = next_input_pattern[:len(pattern['test_si'])].replace('N', 'x')
            print('testpi:' + next_input_pattern)
            bit = 0
            # このまま作成したテストパターンを次のテストパターンとしてもいいが，constraintsで指定したところがドントケア担っている可能性がある
            # そのため，以下で入力と比較して，どんとケアを訂正する
            next_input_pattern = list(next_input_pattern)
            for n, p in zip(next_input_pattern, input_pattern):
                if p != 'x' and n != p:
                    next_input_pattern[bit] = input_pattern[bit]
                bit += 1
            next_input_pattern = ''.join(next_input_pattern)
            input_pattern = next_input_pattern[:]

            print('result:' + input_pattern)


