from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
from string import Template
import os

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv/"

if __name__ == '__main__':
    target   = 'b05'
    stil_f   = target + '.stil'
    si_f     = target + '.test_si'
    output_f = target + '.xfill_stil'

    os.chdir('.temp/')  # よくわからないファイルが出るので作業ディレクトリの変更
    pattern = SortMinTransition.extract_pattern(stil_f)

    f_pattern = []
    with open(si_f, 'r') as f:
        for line in f.readlines():
            print(line)
            f_pattern.append(line.split(' ')[1][:-1])

    for i in range(len(f_pattern)):
        pattern[i]['test_si'] = f_pattern[i]

    output = SortMinTransition.make_initial(stil_f)
    output.extend(SortMinTransition.pattern_to_file(pattern))
    output.extend(SortMinTransition.make_after(stil_f))
    #print(output)
    with open(output_f, 'w') as f:
        for i in output:
            f.write(i)

    #SortMinTransition.x_optimise('stil_c', 'stil_x')
