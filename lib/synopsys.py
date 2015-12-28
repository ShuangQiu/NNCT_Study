import tempfile
import os
import shutil
from string import Template

class Synopsys():
    @staticmethod
    def test():
        print("AAA")

    @staticmethod
    def convertfile(commands):
        temp_f = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp_f.writelines(commands)
        temp_f.close()
        return(temp_f.name)

    @staticmethod
    def combine(template, dic):
        with open(template, 'r') as f:
            s = Template(f.read())
            s = s.substitute(dic)
            print(s)
        return(s)

    @staticmethod
    def system(shell, script, context={}):
        # 辞書の要素数をチェック
        if len(context) >= 1:
            combine = Synopsys.combine(script, context)
            f_name = Synopsys.convertfile(combine)
        if len(context) == 0:
            f_name = Synopsys.convertfile(script)
        for s in ['pt', 'dc', 'tmax']:
            if shell == s and shell =='tmax':
                os.system('tmax -shell -tcl ' + f_name)
            elif shell == s:
                os.system(s + '_shell -f ' + f_name)
                print(s + '_shell -f ' + f_name)

    @staticmethod
    def add_dump_code_in_stildpv(circuit):
        ## stildpv.v ファイルにdumpファイルを生成するプログラムの追加
        already = False
        with open(circuit + '_stildpv.v', 'r') as f:
            stil_file = f.readlines()
        for i in stil_file:
            if 'vector_number = 0;' in i:
                index = stil_file.index(i)
            if '$dumpfile(' in i:
                # すでにdumfileが書かれていた場合
                already = True
        if already != True:
            stil_file.insert(index+1, '$dumpfile("' + circuit + '.vcd");\n')
            stil_file.insert(index+2, '$dumpvars(0, ' + circuit + ');\n')
            with open(circuit + '_stildpv.v', 'w') as f:
                f.writelines(stil_file)

    @staticmethod
    def compute_test_power(context, stil_f="",):
        if stil_f == context['stil'] and context['stil'] != None:
            # stil_f を指定しない時の動作
            os.system('bash ' + context["name"] + '_vcs.sh')
            Synopsys.system(shell='pt', script='../template/AnalysisPower', context=context)

        if stil_f != context['stil']:
            shutil.copy(context["name"] + '.stil', ' .' + context["stil"])
            shutil.copy(stil_f, context["stil"])
   
            settings["power"] = stil_f + '_report_power'
    
            os.system('bash ' + context["name"] + '_vcs.sh')
            Synopsys.system(shell='pt', script='../template/AnalysisPower', context=context)
    
            shutil.copy(' .' + context["stil"], context["stil"])
            os.remove(' .' + context["stil"])
