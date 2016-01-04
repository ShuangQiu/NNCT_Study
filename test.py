from lib.sort_min_transition import SortMinTransition
from lib.verilog import Verilog

if __name__ == '__main__':
    #Verilog.convert_veilog_to_json('b10.vg')
    #Verilog.convert_veilog_to_json('b10.vg', output_f='test.json')
    Verilog.convert_verilog_to_json('controller.v', output_f='test.json')
    #Verilog.convert_verilog_to_json('b10.vg', output_f='test.json')
    Verilog.convert_json_to_verilog('test.json', output_f='test.vg')
    Verilog.extract_comb_circuit_from_verilog_json('test.json', 'after.json')
    Verilog.convert_json_to_verilog('after.json', output_f='after.vg')
    #Verilog.convert_veilog_to_json('b04.vg')

