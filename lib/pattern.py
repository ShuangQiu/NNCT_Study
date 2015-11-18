# import os
import re
import random
import tempfile
from string import Template


class Pattern():
    def __init__(self, target='b10',
                 extension='.stil',
                 directory='/home/lab/matsumoto/Github/Study/Data/output/',
                 fname='.stil',
                 num=0):

        """コンストラクタ
        フォルダ構成
          directory
          --fname
        """
        self.target = target
        self.directory = directory
        self.fname = directory + fname
        self.extension = extension
        self.pattern = []
        self.minTransPattern = []
        self.temp_file = 'temp'
        self.start_file = 'hoge'
        self.end_file = 'hoge'
        self.temp = num

    @staticmethod
    def countTrans(p1, p2):
        """p1とp2の遷移数を調べる

        Return:
        trans:遷移数"""
        trans = 0
        if len(p1) != len(p2):
            raise NameError("please use same length")
        for i in range(len(p1)):
            if p1[i] != p2[i]:
                trans += 1
        return(trans)

    def pull2Patterns(self):
        """STILファイルからテストパターンの抜き出し

        Return:
          pattern(list):
            [test_si, test_so, _pi, _pi2, _po]:
        """
        pattern = []
        temp = []
        frag = False
        # print(self.fname)
        with open(self.fname) as f:
            f = list(f)
            # print(list(enumerate(f)))
            for i, line in enumerate(f):
                if(re.search('"pattern 1"', line)):
                    frag = True
                if not frag:
                    continue
                if(re.search('"test_so"=[LH]*; "test_si"=[01]*', line)):
                    so = re.compile('"test_so"=').search(line)
                    si = re.compile('; "test_si"=').search(line)
                    # print(line[so.end():si.start()])
                    # print(line[si.end():-4])
                    temp.append(line[so.end():si.start()])
                    temp.append(line[si.end():-4])
                elif(re.search('"_pi"=[01P]*; }', line)):
                    pi = re.compile('"_pi"=').search(line)
                    # print(line[pi.end():-4])
                    temp.append(line[pi.end():-4])
                elif(re.search('"_pi"=[01P]*; "_po"=[HL]*;', line)):
                    pi = re.compile('"_pi"=').search(line)
                    po = re.compile('; "_po"=').search(line)
                    # print(line[pi.end():po.start()])
                    # print(line[po.end():-4])
                    temp.append(line[pi.end():po.start()])
                    temp.append(line[po.end():-4])
                elif(re.search('"end [0-9]* unload": ', line)):
                    frag = False
                if len(temp) == 5:
                    pattern.append(temp)
                    temp = []
        self.pattern = pattern
        self.minTransPattern = pattern
        # print(self.minTransPattern)
        # print("------")
        return(pattern)

    def makeSTILTemplate(self):
        """STILファイルを読み込みTemplateファイルの作成

        Return:
          Templateファイルが書かれた一時ファイル
          最初の初期設定ファイル + pattern + 最後の締めファイル"""
        ftemp = []
        frag = True
        with open(self.fname) as f:
            for line in f:
                if(re.search('Ann {\* fast_sequential \*}', line)
                   ) and frag:
                    frag = False
                    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
                    f.writelines(ftemp)
                    self.start_file = f.name
                    f.close()
                    # print(ftemp)
                    ftemp = []
                if(re.search('"end [0-9]* unload": ', line)):
                    frag = True
                if not frag:
                    continue
                ftemp.append(line)
            else:
                ftemp.insert(0, '   Ann {* fast_sequential *}\n')
                f = tempfile.NamedTemporaryFile(mode='w', delete=False)
                f.writelines(ftemp)
                self.end_file = f.name
                f.close()
                # print(ftemp)
                ftemp = []
        return()

    def makeSTIL(self):
        """STILファイルを作成
        事前にTemplateファイルを作成しといたらいいと思う
        """
        pattern = []
        output = []
        template_pattern = '   Ann {* fast_sequential *}\n'\
            + '   "pattern ${num}": Call "load_unload" { \n'\
            + '      "test_so"=${so}; "test_si"=${si}; } \n'\
            + '   Call "allclock_launch" {\n'\
            + '      "_pi"=${first_pi}; }\n'\
            + '   Call "allclock_capture" {\n'\
            + '      "_pi"=${second_pi}; "_po"=${po};}\n'
        t = Template(template_pattern)
        for i, j in enumerate(self.minTransPattern):
            pattern.append(t.substitute(num=str(i+1), so=j[0], si=j[1],
                                        first_pi=j[2], second_pi=j[3],
                                        po=j[4]))
        for line in open(self.start_file):
            output.append(line)
        output.extend(pattern)
        for line in open(self.end_file):
            output.append(line)
        f = open(self.directory + self.target + '_sorted' + str(self.temp)
                 + self.extension, 'w')
        self.temp += 1
        f.writelines(output)
    
    def shufflePattern(self):
        """listをシャッフルして遷移数が少ないのを求める

        Return:
          trans:遷移数
        """
        self.makeSTILTemplate()
        self.pull2Patterns()
        trans = 0
        pattern = self.pattern
        for i in range(len(pattern) - 1):
            trans += self.countTrans(pattern[i][3], pattern[i+1][2])
        print(trans)
        # for j in range(1000):
        while True:
            random.shuffle(pattern)
            tmp_trans = 0
            for i in range(len(pattern) - 1):
                tmp_trans += self.countTrans(pattern[i][3], pattern[i+1][2])
            if tmp_trans < trans:
                trans = tmp_trans
                self.minTransPattern = list(pattern)
                self.makeSTIL()
                print(trans)
        print(trans)
        return(trans)

    def makeSTILstep(self):
        """STILファイルを1パタン, 2パタン, 3パタンと順番にする
        事前にTemplateファイルを作成しといたらいいと思う
        """
        self.makeSTILTemplate()
        self.pull2Patterns()
        pattern = []
        output = []
        template_pattern = '   Ann {* fast_sequential *}\n'\
            + '   "pattern ${num}": Call "load_unload" {\n'\
            + '      "test_so"=${so}; "test_si"=${si}; }\n'\
            + '   Call "allclock_launch" {\n'\
            + '      "_pi"=${first_pi}; }\n'\
            + '   Call "allclock_capture" {\n'\
            + '      "_pi"=${second_pi}; "_po"=${po};}\n'
        t = Template(template_pattern)
        for k in range(len(self.minTransPattern) + 1):
            for i, j in enumerate(self.minTransPattern):
                if i == k:
                    break
                pattern.append(t.substitute(num=str(i+1), so=j[0], si=j[1],
                                            first_pi=j[2], second_pi=j[3],
                                            po=j[4]))
            for line in open(self.start_file):
                output.append(line)
            output.extend(pattern)
            for line in open(self.end_file):
                output.append(line)
            f = open(self.directory + 'temp/' + self.target + '_' + str(k) + self.extension, 'w')
            f.writelines(output)
            output = list([])
            pattern = list([])
