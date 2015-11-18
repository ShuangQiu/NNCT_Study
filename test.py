from lib.sort_min_transition import SortMinTransition
import os


if __name__ == '__main__':

    os.chdir('.temp')  # よくわからないファイルが出るので作業ディレクトリの変更
    SortMinTransition.sort('b04.stil', 'b04_sort.stil')
