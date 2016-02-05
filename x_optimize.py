from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
from string import Template
import os

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv/"

if __name__ == '__main__':
    target   = 'b05'
    stil_f = target + '.xfill_stil'
    output_f = target + '.xoptimise.stil'

    os.chdir('.temp/')  # よくわからないファイルが出るので作業ディレクトリの変更

    SortMinTransition.x_optimise(stil_f, output_f)
