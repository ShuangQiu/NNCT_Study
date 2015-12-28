import tempfile
import os
import shutil
from string import Template

class Verilog():
    @staticmethod
    def perse_veilog_to_json(verilog_f, output_f=''):
        # 構造
        # {
        #   "module" : [
        #       {
        #           "module_name": 'b01', 
        #           "argument":  [
        #               "r_button",
        #               "g_button",
        #               ....
        #           ],
        #           "input": {   # ビット数をキー値としている
        #               0 : [
        #                   "r_button",
        #                   "g_button"
        #               ],
        #               1: [],
        #               ...
        #               4: [
        #                   "v_in",
        #               ]
        #           },
        #           "output": {   # ビット数をキー値としている
        #               0 : [
        #                   "cts",
        #                   "ctr"
        #               ],
        #               1: [],
        #               ...
        #               4: [
        #                   "v_out",
        #               ]
        #           }
        #           "wire": {   # ビット数をキー値としている
        #               0 : [
        #                   "voto0",
        #                   "n17"
        #               ],
        #               1: [],
        #               ...
        #               4: [
        #                   "stato",
        #               ]
        #           },
        #           "gate": [
        #               {
        #                   "gate_name": "INV_X4",
        #                   "module_name": "U19",
        #                   "argument" : {
        #                       ".A": "reset",
        #                       ".ZN": "n17"
        #                   }
        #               },
        #               {
        #                   "gate_name": "NAND2_X2",
        #                   "module_name": "U22",
        #                   "argument" : {
        #                       ".A1": "ctr",
        #                       ".A2": "n55",
        #                       ".B1": "n59",
        #                       ".B2": "n60",
        #                       ".ZN": "n58"
        #                   }
        #               }
        #           ]
        #       }
        #   ]
        #}
        print('ok')
        

