import tempfile
import os
import shutil
from string import Template

class Verilog():
    @staticmethod
    def perse_veilog_to_json(verilog_f, output_f=''):
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
        print('ok')
        with open(verilog_f, "r") as f:
            # 一行ずつ読み込む
            append_line = ''
            for line in f:
                # セミコロンまでに複数にわかれている行を一行に変換する
                append_line += line[:-1].strip()

                if ';' in line or 'endmodule' in line:
                    judge_word = append_line.split(' ', 1)[0]
                    #print(judge_word + ' ', end='')
                    if judge_word == 'module':
                        verilog_dict = Verilog.perse_module_begin_line(append_line)
                        print(verilog_dict)
                    elif judge_word == 'output' or judge_word == 'input' or judge_word == 'wire':
                        # する必要がなくなったのでしていない
                        pass
                    if judge_word == 'endmodule':
                        # する必要がなくなったのでしていない
                        pass
                    else:
                        # する必要がなくなったのでしていない
                        pass
                    append_line = ''

    def perse_module_begin_line(line):
        perse_result = {}
        module_argument = []
        split_space_list = line.split(' ')
        perse_result[split_space_list[1]] = {}
        perse_result[split_space_list[1]]['argument'] = []

        # ( )の間のリストを取得するための処理
        parenth_begin = split_space_list.index('(')
        parenth_end = split_space_list.index(');')

        for arg in split_space_list[parenth_begin + 1:parenth_end]:
            perse_result[split_space_list[1]]['argument'].append(arg)
        return perse_result
