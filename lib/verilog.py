import tempfile
import os
import shutil
import re
import json
import collections
from string import Template

        # 構造
        # {
        #   "module_name" : [
        #       {
        #           'b01' : {
        #               "argument":  [
        #                   "r_button",
        #                   "g_button",
        #                   ....
        #               ],
        #               "input": {   # ビット数をキー値としている
        #                   0 : [
        #                       "r_button",
        #                       "g_button"
        #                   ],
        #                   1: [],
        #                   ...
        #                   4: [
        #                       "v_in",
        #                   ]
        #               },
        #               "output": {   # ビット数をキー値としている
        #                   0 : [
        #                       "cts",
        #                       "ctr"
        #                   ],
        #                   1: [],
        #                   ...
        #                   4: [
        #                       "v_out",
        #                   ]
        #               }
        #               "wire": {   # ビット数をキー値としている
        #                   0 : [
        #                       "voto0",
        #                       "n17"
        #                   ],
        #                   1: [],
        #                   ...
        #                   4: [
        #                       "stato",
        #                   ]
        #               },
        #               "gate": [
        #                   {
        #                       "gate_name": "INV_X4",
        #                       "module_name": "U19",
        #                       "argument" : {
        #                           ".A": "reset",
        #                           ".ZN": "n17"
        #                       }
        #                   },
        #                   {
        #                       "gate_name": "NAND2_X2",
        #                       "module_name": "U22",
        #                       "argument" : {
        #                           ".A1": "ctr",
        #                           ".A2": "n55",
        #                           ".B1": "n59",
        #                           ".B2": "n60",
        #                           ".ZN": "n58"
        #                       }
        #                   }
        #               ]
        #       }
        #   ]
        #}

class Verilog():
    @staticmethod
    def convert_verilog_to_json(verilog_f, output_f=''):
        # Verilog File を json ファイルにコンバートする
        with open(verilog_f, "r") as f:
            # 一行ずつ読み込む
            append_line = ''
            for line in f:
                # セミコロンまでに複数にわかれている行を一行に変換する
                append_line += line[:-1].strip()
                if ';' in line or 'endmodule' in line:
                    append_line = re.split('[\s,;]+?', append_line)
                    append_line = list(filter(lambda w: len(w) > 0, append_line))
                    append_line = list(append_line)
                    judge_word =  append_line[0]
                    
                    if judge_word == 'module':
                        module_name, verilog_perse_result = Verilog.perse_first_module_line(append_line)
                        verilog_perse_result[module_name]['input'] = {}
                        verilog_perse_result[module_name]['output'] = {}
                        verilog_perse_result[module_name]['wire'] = {}
                        verilog_perse_result[module_name]['assign'] = {}
                        verilog_perse_result[module_name]['gates'] = []
                    elif judge_word == 'output' or judge_word == 'input' or judge_word == 'wire':
                        verilog_perse_result[module_name][judge_word].update(Verilog.perse_wire_outinput_line(append_line))
                    elif judge_word == 'assign':
                        verilog_perse_result[module_name][judge_word].update(Verilog.perse_assign_line(append_line))
                    elif judge_word == 'endmodule':
                        pass
                    else:
                        # gate line 
                        verilog_perse_result[module_name]['gates'].append(Verilog.perse_gate_line(append_line))
                        pass
                    append_line = ''
                if append_line != '':
                    append_line += ' '
        if output_f == '':
            print(json.dumps(verilog_perse_result, indent=4))
        if len(output_f) >= 1:
            with open(output_f, 'w') as fp:
                json.dump(verilog_perse_result, fp, indent=4)

    @staticmethod
    def perse_first_module_line(line_split_list):
        perse_result = collections.OrderedDict()
        module_argument = []
        line_split_iter = iter(line_split_list)
        while True:
            word = next(line_split_iter)
            if word == '(':
                while True:
                    argument = next(line_split_iter)
                    if  argument == ')':
                        break
                    module_argument.append(argument)
                break
        perse_result[line_split_list[1]] = collections.OrderedDict()
        perse_result[line_split_list[1]]['argument'] = module_argument

        return (line_split_list[1], perse_result)

    @staticmethod
    def perse_wire_outinput_line(line_split_list):
        # wire, output, input lineをperse
        perse_result = {}

        if re.search('\[[0-9]+:[0-9]\]', line_split_list[1]):
            match_num = re.search('[0-9]', line_split_list[1]);
            signal_num = int(match_num.group(0))
            perse_result[signal_num] = line_split_list[2:]
        else:
            signal_num = 0
            perse_result[signal_num] = line_split_list[1:]
        return(perse_result)

    @staticmethod
    def perse_assign_line(line_split_list):
        # assing line を perse
        perse_result = {}
        perse_result[line_split_list[1]] = line_split_list[3]
        return(perse_result)

    @staticmethod
    def perse_gate_line(line_split_list):
        # gate の書かれている文をperse
        perse_result = collections.OrderedDict()
        perse_result['gate'] = line_split_list[0]
        perse_result['name'] = line_split_list[1]
        perse_result['argument'] = collections.OrderedDict()
        line_split_iter = iter(line_split_list)
        
        # 一度行に戻す
        arg_line = ''
        arg_list = []
        for line in line_split_list[3:-1]:
            arg_line += line
        arg_list = re.split('\.', arg_line)
        arg_list = list(filter(lambda w: len(w) > 0, arg_list))
        for li in arg_list:
            li_iter = iter(li)
            key = ''
            argument = ''
            while True:
                key_char = next(li_iter)
                if '(' == key_char:
                    while True:
                        arg_char = next(li_iter)
                        if ')' == arg_char:
                            break
                        argument += arg_char
                    break
                key += key_char
            perse_result['argument'][key] = argument
        return(perse_result)

    @staticmethod
    def convert_json_to_verilog(json_f, output_f=''):
        result_list = []
        with open(json_f, 'r') as fp:
            input_json_dict = json.loads(fp.read(), object_pairs_hook=collections.OrderedDict)
            for module_name in input_json_dict:
                for module_object in input_json_dict[module_name]:
                    if module_object == 'argument':
                        result_list.append(Verilog.convert_argument_to_sentence(module_name, input_json_dict[module_name][module_object]))
                    elif module_object == 'output' or module_object == 'input' or module_object == 'wire':
                        result_list.append(Verilog.convert_outinput_wire_to_sentence(module_object, input_json_dict[module_name][module_object]))
                    elif module_object == 'assign':
                        result_list.append(Verilog.convert_assign_to_sentence(input_json_dict[module_name][module_object]))
                    elif module_object == 'gates':
                        result_list.append(Verilog.convert_gate_to_sentence(input_json_dict[module_name][module_object]))
                else:
                    result_list.append('endmodule')
        if output_f == '':
            for i in result_list:
                print(i)
        if len(output_f) >= 1:
            with open(output_f, 'w') as fp:
                for i in result_list:
                    fp.write(i)
                    fp.write('\n')

    @staticmethod
    def convert_argument_to_sentence(module_name, module_argument):
        result_sentence = 'module ' + module_name + ' ('
        for arg in module_argument:
            result_sentence += ' ' + arg + ','
        result_sentence = result_sentence[:-1] + ' );\n'
        return(result_sentence)

    @staticmethod
    def convert_outinput_wire_to_sentence(module_object, module_argument):
        result_sentence = ''
        for port_num in module_argument:
            argument_word = '  ' + module_object
            if port_num != '0':
                argument_word += ' [' + port_num + ':0]'
            for arg in module_argument[port_num]:
                argument_word += ' ' +  arg + ','
            result_sentence += argument_word[:-1] + ';\n'
            argument_word = ''
        return(result_sentence)

    @staticmethod
    def convert_assign_to_sentence(module_argument):
        result_sentence = ''
        for arg_left in module_argument:
            result_sentence += '  assign ' + arg_left + ' = ' + module_argument[arg_left] + ';\n'
        return(result_sentence)

    @staticmethod
    def convert_gate_to_sentence(module_argument):
        result_sentence = ''
        for arg in module_argument:
            arg_sentence = '  ' + arg['gate'] + ' ' + arg['name'] + ' ('
            for arg_key, arg_value in arg['argument'].items():
                arg_sentence += ' .' + arg_key + '(' + arg_value + '),'
            arg_sentence = arg_sentence[:-1] + ' );\n'
            result_sentence += arg_sentence
        return(result_sentence)

    @staticmethod
    def extract_comb_circuit_from_verilog_json(json_f, output_f=''):
        ff_count = 0
        not_gate_name = ''
        not_gate_input_arg_name = ''
        not_gate_output_arg_name = ''
        with open(json_f, 'r') as fp:
            input_json_dict = json.loads(fp.read(), object_pairs_hook=collections.OrderedDict)
            for module_name in input_json_dict:
                module_dict = input_json_dict[module_name]
                # NOTゲートの名前判定 判定基準 argumentの数が２つのもの
                for gate in module_dict['gates']:
                    if len(gate['argument']) == 2:
                        not_gate_name = gate['gate']
                        not_gate_input_arg_name = list(gate['argument'].keys())[0]
                        not_gate_output_arg_name = list(gate['argument'].keys())[1]
                        break
                # FFの数を求める 判定基準 Q または QNを持っているか
                # 組み合わせ回路になるように追加するpinの接続状況を更新
                del_gate_num = []
                for num, gate in enumerate(module_dict['gates']):
                    if 'Q' in gate['argument'] or 'QN' in gate['argument']:
                        module_dict['assign'][ gate['argument']['Q'] ] = 'ppi_ps_reg[' + str(ff_count) + ']'
                        module_dict['assign'][ 'ppo_ps_reg[' + str(ff_count) + ']' ] = gate['argument']['D']
                        # QN につなぐNOT ゲートの作成
                        connect_qn_gate = collections.OrderedDict()
                        connect_qn_gate['gate'] = not_gate_name
                        connect_qn_gate['name'] = 'UN' + str(ff_count)
                        connect_qn_gate['argument'] = collections.OrderedDict()
                        connect_qn_gate['argument'][not_gate_input_arg_name] = 'ppi_ps_reg[' + str(ff_count) + ']'
                        connect_qn_gate['argument'][not_gate_output_arg_name] = gate['argument']['QN']
                        module_dict['gates'].append(connect_qn_gate)
                        ff_count += 1
                        del_gate_num.append(num)
                # いらないFFを削除
                del_gate_num.sort(reverse=True)
                for num in del_gate_num:
                    del module_dict['gates'][num]
                # FFの数だけoutputとinputを定義
                str_ff_count = str(ff_count - 1)
                if str_ff_count in module_dict['input']:
                    module_dict['input'][str_ff_count].append('ppi_ps_reg')
                elif not str_ff_count in module_dict['input']:
                    module_dict['input'][str_ff_count] = [ 'ppi_ps_reg' ]
                if str_ff_count in module_dict['output']:
                    module_dict['output'][str_ff_count].append('ppi_ps_reg')
                elif not str_ff_count in module_dict['output']:
                    module_dict['output'][str_ff_count] = [ 'ppi_ps_reg' ]
                # moduleのargument に ppi_ps_reg等を追加
                module_dict['argument'].append('ppi_ps_reg')
                module_dict['argument'].append('ppo_ps_reg')
        if output_f == '':
            print(json.dumps(input_json_dict, indent=4))
        if len(output_f) >= 1:
            with open(output_f, 'w') as fp:
                json.dump(input_json_dict, fp, indent=4)
