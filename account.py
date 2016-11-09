import re

class Account:
    def __init__(self, login):
        self.login = login

    def get_info(html):
        village_vids_compile = re.compile('\?newdid=(\d+)')
        village_vids = village_vids_compile.findall(html)
        print('vids', village_vids)
        village_amount = len(village_vids)
        print('amount', village_amount)
        nation_compile = re.compile('nation(\d)')
        nation = nation_compile.findall(html)[0]
        print('nation', nation)
        x_compile = re.compile('coordinateX">\(&#x202d;&(#45;)*&*#x202d;(\d+)')
        X = x_compile.findall(html)
        y_compile = re.compile('coordinateY">&#x202d;&(#45;)*&*#x202d;(\d+)')
        Y = y_compile.findall(html)
        pos = []
        for i in range(len(X)):
            p = [0, 0]
            if '#45' in X[i][0]:
                p[0] = -int(X[i][1])
            else:
                p[0] = int(X[i][1])
            if '#45' in Y[i][0]:
                p[1] = -int(Y[i][1])
            else:
                p[1] = int(Y[i][1])
            pos.append(p)
        print('pos', pos)
        ajax_token_compile = re.compile('ajaxToken\s*=\s*\'(\w+)\'')
        ajax_token = ajax_token_compile.findall(html)[0]
        print('ajax token', ajax_token)

