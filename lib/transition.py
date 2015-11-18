import random

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
                print(check, pattern)
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

if __name__ == '__main__':
    patterns = []  # テストパターン
    path = []  # パス

    # 初期化
    ########
    target = 'b13'
    with open('Patterns/'+target+'_before', encoding='utf-8') as file_pattern:
        num = 0
        patterns.append(FirstPattern(capture=file_pattern.readline()[:-1]))
        for fp in file_pattern:
            print(fp)
            num += 1
            pattern = Pattern(num=num,\
                              launch=fp[:-1],\
                              capture=next(file_pattern)[:-1])
            patterns.append(pattern)

    print('=' * 10)
    print('launch', 'capture')
    for i in patterns:
        print(i.launch, i.capture)
    print('=' * 10)

    # 重み比較
    ##########
    max_weight = 0
    for i, p1 in enumerate(patterns):
        for j, p2 in enumerate(patterns[1:]):
            if i != j+1:
                weight = len([0 for x, y in zip(p1.capture, p2.launch) if x != y])
                max_weight = weight if max_weight < weight else max_weight
                print(p1.capture, p2.launch, weight)
                path.append((i, j+1, weight))
    for i in path:
        print(i)
    print('=' * 10)

    # 最小毎にパスを接続
    ####################
    for weight in range(max_weight + 1):
        connect_path(patterns, path, weight)

    # 結果
    ######
    for i, p in enumerate(patterns):
        print(i, p.connect, p, p.next_connect, p.back_connect)
    print('=' * 10)

    circuit = target
    target = patterns[0]
    trans = 0
    f = open('Patterns/'+circuit+'_after', 'w')
    ft = open('Patterns/'+circuit+'_trans', 'w')
    for i in range(len(patterns) - 1):
        print(str(target.num), target.launch, target.capture)
        if target.launch != None:
            f.write(str(target.num) + '\n' + target.launch + '\n' + target.capture + '\n')
            ft.write(target.launch + '\n' + target.capture + '\n')
        else:
            f.write(str(target.num) + '\n' + target.capture + '\n')
            ft.write(target.capture + '\n')
        temp = target.capture
        target = target.next_connect
        trans += get_trans(temp, target.launch)

    print(trans)
