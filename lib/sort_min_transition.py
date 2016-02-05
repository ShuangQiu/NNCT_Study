from string import Template
import random
import os
import re

class TestPattern():
    def __init__(self, num, launch, capture):
        self.num = num
        self.launch = launch
        self.capture = capture
        self.connect = 0
        self.next_connect = None
        self.back_connect = None

    def connect_next_pattern(self, pattern):
        if self.next_connect == None and pattern.back_connect == None:
            check = self.back_connect
            while check != None:
                #print(check, pattern)
                if check == pattern:
                    break
                check = check.back_connect
            else:
                self.next_connect = pattern
                pattern.back_connect = self
                self.connect += 1

class FirstPattern(TestPattern):
    def __init__(self, capture):
        super().__init__(num=0, launch=None, capture=capture)
        self.launch = None

class Pattern(TestPattern):
    def __init__(self, num, launch, capture):
        super().__init__(num, launch, capture)

def extract_path_have_weight(path, weight):
    # 最小の重み抜き出し
    ####################
    weight_path = []
    for p in path:
        if p[2] == weight:
            weight_path.append(p)
    # print(weight_path)
    return(weight_path)

def extract_path_connected(path):
    # 接続候補数の抽出
    num_connected = {}
    for p in path:
        # pick_num_connect[p[0]] = 0 if pick_num_connect in p
        num_connected[p[1]] = 0 if not p[1] in num_connected else num_connected[p[1]]
        num_connected[p[1]] += 1
    return(sorted(num_connected.items(), key=lambda x:x[1]))

def make_random_list(num):
    ran = []
    while num != len(ran):
        ran.append(random.randrange(num))
        ran = sorted(set(ran), key=ran.index)
    return ran

def get_trans(p1, p2):
    trans = 0
    for i, j in zip(p1, p2):
        trans = trans + 1 if i != j else trans
    return(trans)

def connect_path(patterns, path, weight):
    target = 0
    light_path = extract_path_have_weight(path=path, weight=weight)
    pick_num_connect = extract_path_connected(path=light_path)
    # つなげるパスの選択
    ####################
    light_path = sorted(light_path, key=lambda x:x[1])
    for path, num in pick_num_connect:
        for i, p in enumerate(light_path):
            if path == p[1]:
                target = i
                break
        if num == 1:
            connect = light_path[target]
            patterns[connect[0]].connect_next_pattern(patterns[connect[1]])
        elif num >= 2:
            rans = make_random_list(num)
            for ran in rans:
                connect = light_path[target + ran]
                patterns[connect[0]].connect_next_pattern(patterns[connect[1]])

def make_initial(input_f):
    # 入力のSTILファイルを基にSTILのテストパターン部分以前の作成
    # Retun Listファイル
    output = []
    count = 0
    with open(input_f) as f:
        for line in f:
            if re.search('Ann {\* fast_sequential \*}', line):
                count += 1
                if count == 1:
                    break;
            else:
                output.append(line)
    return output

def make_after(input_f):
    # 入力のSTILファイルを基にSTILのテストパターン部分以後の作成
    # Retun Listファイル
    # Patternの0つ目も含める
    output = []
    f_list = []
    with open(input_f) as f:
        for line in f:
            f_list.append(line)
    output.extend(f_list[-6:])
    return output

def make_testpattern(input_f):
    pattern_l = extract_pattern(input_f)
    patterns = []
    path = []

    # 並び替えアルゴリズム
    #temp = pattern_l[0]['pi_2']
    #for i in pattern_l[1:]:
    #    print(temp, i['pi_1'])
    #    temp = i['pi_2']
    num = 0
    patterns.append(FirstPattern(capture=pattern_l[0]['pi_2']))
    #print(patterns[0].capture)
    for fp in pattern_l[1:]:
        #print(fp)
        num += 1
        pattern = Pattern(num=num,\
                          launch=fp['pi_1'],\
                          capture=fp['pi_2'])
        patterns.append(pattern)

    #print('=' * 10)
    #print('launch', 'capture')
    #for i in patterns:
    #    print(i.launch, i.capture)
    #print('=' * 10)

    # 重み比較
    ##########
    max_weight = 0
    for i, p1 in enumerate(patterns):
        for j, p2 in enumerate(patterns[1:]):
            if i != j+1:
                weight = len([0 for x, y in zip(p1.capture, p2.launch) if x != y])
                max_weight = weight if max_weight < weight else max_weight
                #print(p1.capture, p2.launch, weight)
                path.append((i, j+1, weight))
    #for i in path:
    #    print(i)
    #print('=' * 10)

    # 最小毎にパスを接続
    ####################
    for weight in range(max_weight + 1):
        connect_path(patterns, path, weight)

    # 結果
    ######
    #for i, p in enumerate(patterns):
    #    print(i, p.connect, p, p.next_connect, p.back_connect)
    #print('=' * 10)

    # 結果をリストにする
    target = patterns[0]
    trans = 0
    n_pattern_l =  []
    #for i in range(len(patterns) - 1):
    for i, j in enumerate(patterns):
        #print(str(target.num), target.launch, target.capture)
        n_pattern_l.append(pattern_l[target.num])
        #print(pattern_l[target.num])
        temp = target.capture
        target = target.next_connect
        if i == len(patterns) - 1:
            break
        trans += get_trans(temp, target.launch)
   
    output = pattern_to_file(n_pattern_l)
    #print(trans)
    return(output)


def make_optimise_x(input_f):
    pattern_l = extract_pattern(input_f)
    output = []
    path = []

    # Nの最適化
    word = '0'
    for pattern in pattern_l:
        for p_name in ['pi_1', 'pi_2', 'test_si']:
            pat = ''
            for p in pattern[p_name]:
                if p == 'N' or p == 'x':
                    pat += word
                elif p == 'P':
                    pat += p
                else:
                    word = p
                    pat += p
            pattern[p_name] = pat
    output = pattern_to_file(pattern_l)
    return(output)

def make_optimise_random(input_f):
    pattern_l = extract_pattern(input_f)
    output = []
    path = []

    # Nの最適化
    word = '0'
    for pattern in pattern_l:
        for p_name in ['pi_1', 'pi_2', 'test_si']:
            pat = ''
            for p in pattern[p_name]:
                if p == 'N':
                    word = str(random.randrange(2))
                    pat += word
                elif p == 'P':
                    pat += p
                else:
                    word = p
                    pat += p
            pattern[p_name] = pat
    output = pattern_to_file(pattern_l)
    return(output)


def pattern_to_file(input_l):
    # 入力List[test_so,test_si,pi,pi,po]をテストパターンのリストに置き換える
    # 入力List[{test_so='aaaa',..},{..}]
    output = []
    template = Template('   Ann {* fast_sequential *}\n' + \
                        '   "pattern ${num}": Call "load_unload" { \n' + \
                        '      "test_so"=${test_so}; ' + \
                        '"test_si"=${test_si}; }\n' + \
                        '   Call "${launch}" { \n' + \
                        '      "_pi"=${pi_1}; }\n' + \
                        '   Call "${capture}" { \n' + \
                        '      "_pi"=${pi_2}; "_po"=${po}; }\n')
    template_first = Template('   Ann {* fast_sequential *}\n' + \
                        '   "pattern ${num}": Call "load_unload" { \n' + \
                        '      "test_si"=${test_si}; }\n' + \
                        '   Call "${launch}" { \n' + \
                        '      "_pi"=${pi_1}; }\n' + \
                        '   Call "${capture}" { \n' + \
                        '      "_pi"=${pi_2}; "_po"=${po}; }\n')

    for i, l in enumerate(input_l):
        l['num'] = i
        if i == 0:
            line = template_first.substitute(l)
            output.append(line)
        else:
            #l['num'] = i + 1
            line = template.substitute(l)
            output.append(line)
    return(output)

def generate_pattern(input_f):
    # Generator input_fの
    with open(input_f) as f:
        for i in f:
            yield i

def extract_pattern(input_f):
    # STILファイルからテストパターンの抜き出し
    # Return: List
    temp = {}
    frag = False
    pattern = generate_pattern(input_f)
    output = []

    while True:
        # 1パターン前まで飛ばす処理
        if re.search('Ann {\* fast_sequential \*}', next(pattern)):
            break
    frag = True
    while frag:
        word = ''
        while True:
            # テストパターンを一つの行にまとめる(改行対策)
            line = next(pattern)
            word += str(line)[:-1]
            if re.search('Ann {\* fast_sequential \*}', line):
                break
            if re.search('"end', line):
                frag = False
                break
        # 一行にまとめた中からテストパターンの抽出
        if frag == True:
            si = re.compile(';').finditer(word)
            if(re.search('"test_so"=[LHX]*;', word)):
                so = re.compile('"test_so"=').search(word)
                temp['test_so'] = word[so.end():next(si).start()]
            if(re.search('"test_si"=[10PNx]*;', word)):
                so = re.compile('"test_si"=').search(word)
                temp['test_si'] = word[so.end():next(si).start()]
            pi = re.compile('"_pi"=').finditer(word)
            if(re.search('"_pi"=', word)):
                temp['pi_1'] = word[next(pi).end():next(si).start()]
            if(re.search('"_pi"=', word)):
                temp['pi_2'] = word[next(pi).end():next(si).start()]
            if(re.search('"_po"=[HLX]*;', word)):
                so = re.compile('"_po"=').search(word)
                temp['po'] = word[so.end():next(si).start()]
            # clock launch
            clock = re.compile('Call "[a-zA-Z0-9_]+" {').finditer(word)
            if(re.search('Call ', word)):
                call = re.compile('Call "[a-zA-Z0-9_]+" {').finditer(word)
                next(clock);next(call)
                temp['launch'] = word[next(call).start() + 6:next(clock).end() - 3]
                temp['capture'] = word[next(call).start() + 6:next(clock).end() - 3]
            output.append(temp)
        temp = {}
    return(output)


class SortMinTransition():
    def sort(input_f, output_f):
        output = make_initial(input_f)
        output.extend(make_testpattern(input_f))
        output.extend(make_after(input_f))
        with open(output_f, 'w') as f:
            for i in output:
                f.write(i)

    def x_optimise(input_f, output_f):
        output = make_initial(input_f)
        output.extend(make_optimise_x(input_f))
        output.extend(make_after(input_f))
        with open(output_f, 'w') as f:
            for i in output:
                f.write(i)

    def random_optimise(input_f, output_f):
        output = make_initial(input_f)
        output.extend(make_optimise_random(input_f))
        output.extend(make_after(input_f))
        with open(output_f, 'w') as f:
            for i in output:
                f.write(i)

    def trans(input_f):
        trans = 0
        pattern_l = extract_pattern(input_f)
        p1 = pattern_l[0]['pi_2']
        for i in pattern_l[1:]:
            p2 = i['pi_1']
            trans += get_trans(p1, p2)
            p1 = i['pi_2']
        return trans

    def pattern_num(input_f):
        pattern_l = extract_pattern(input_f)
        return len(pattern_l)

    def make_initial(input_f):
        return make_initial(input_f)

    def extract_pattern(input_f):
        return extract_pattern(input_f)

    def make_after(input_f):
        return make_after(input_f)

    def pattern_to_file(input_f):
        return pattern_to_file(input_f)

    # 以下の階層は 後で整理しましょう
    def extract_pattern_comb(input_f):
        # STILファイルからテストパターンの抜き出し
        # Return: List
        temp = {}
        frag = False
        pattern = generate_pattern(input_f)
        output = []
    
        while True:
            # 1パターン前まで飛ばす処理
            if re.search('Macro "test_setup";', next(pattern)):
                break
        frag = True
        while frag:
            word = ''
            while True:
                # テストパターンを一つの行にまとめる(改行対策)
                line = next(pattern)
                word += str(line)[:-1]
                if re.search('^}', line):
                    break
                if re.search('Patterns reference', line):
                    frag = False
                    break
            # 一行にまとめた中からテストパターンの抽出
            if frag == True:
                si = re.compile(';').finditer(word)
                if(re.search('"test_so"=[LHX]*;', word)):
                    so = re.compile('"test_so"=').search(word)
                    temp['test_so'] = word[so.end():next(si).start()]
                if(re.search('"test_si"=[10PN]*;', word)):
                    so = re.compile('"test_si"=').search(word)
                    temp['test_si'] = word[so.end():next(si).start()]
                pi = re.compile('"_pi"=').finditer(word)
                if(re.search('"_pi"=', word)):
                    temp['pi'] = word[next(pi).end():next(si).start()]
                if(re.search('"_po"=[HLX]*;', word)):
                    so = re.compile('"_po"=').search(word)
                    temp['po'] = word[so.end():next(si).start()]
                # clock launch
                output.append(temp)
            temp = {}
        return(output)


if __name__ == '__main__':
    os.chdir('../')  # よくわからないファイルが出るので作業ディレクトリの変更
    SortMinTransition.x_optimise('stil', 'stil_x')
#    SortMinTransition.sort('b04.stil', 'b04_sort.stil')
#    print(SortMinTransition.trans('b04.stil'))
#    print(SortMinTransition.trans('b04_sort.stil'))
    #print(SortMinTransition.extract_pattern('stil'))
