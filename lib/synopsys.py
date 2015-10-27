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
    def dc_shell(commands):
        f_name = Synopsys.convertfile(commands)
        os.system('dc_shell -f ' + f_name)
        os.remove(f_name)

    @staticmethod
    def pt_shell(commands):
        f_name = Synopsys.convertfile(commands)
        os.system('pt_shell -f ' + f_name)
        os.remove(f_name)

    @staticmethod
    def tmax(commands):
        f_name = Synopsys.convertfile(commands)
        os.system('tmax -shell -tcl ' + f_name)
        os.remove(f_name)

    @staticmethod
    def combine(template, dic):
        with open(template, 'r') as f:
            s = Template(f.read())
            s = s.substitute(dic)
        return(s)
