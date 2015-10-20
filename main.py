from lib.synopsys import Synopsys
from string import Template


if __name__ == '__main__':
    Synopsys.test()

    dic_logic = dict(db='aaa',
                     target='aaa',
                     name='aaa',
                     output_vg='aaa',
                     output_spf='aaa',
                     )

    with open('./template/LogicSynthesis', 'r') as f:
        s = Template(f.read())
        s = s.substitute(dic_logic)
        Synopsys.dc_shell(s)
