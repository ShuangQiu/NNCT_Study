from lib.synopsys import Synopsys
from lib.sort_min_transition import SortMinTransition
from string import Template
import os

def settings_path():
    os.environ["STILDPV_HOME"] = "/cad/Synopsys/TetraMax/E-2010.12-SP2/linux/stildpv/"

if __name__ == '__main__':
    target   = 'b10'
    os.chdir('.temp/')  # よくわからないファイルが出るので作業ディレクトリの変更


    # ランダム割り当て
    stil_f = target + '.stil'
    output_f = target + '.randomoptimise.stil'
    SortMinTransition.random_optimise(stil_f, output_f)

    # 単純にX割り当て
    stil_f = target + '.stil'
    output_f = target + '.xoptimise.stil'
    SortMinTransition.x_optimise(stil_f, output_f)

    # X割り当て
    stil_f = target + '.xfill_stil'
    output_f = target + '.proposexoptimise.stil'
    SortMinTransition.x_optimise(stil_f, output_f)
