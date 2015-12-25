import tempfile
import os
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
