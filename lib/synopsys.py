import tempfile
import os

class Synopsys():
    @staticmethod
    def test():
        print("AAA")

    @staticmethod
    def dc_shell(commands):
        temp_f = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp_f.writelines(commands)
        temp_f.close()
        os.system('dc_shell -f ' + temp_f.name)
        os.remove(temp_f.name)
