import sys
import os
import re
import time
import random
import subprocess


#refer: http://www.36fengshui.com/bz/bz61.asp
DAJI_STROKE_NUMBER = {
    '首领数':[3, 16, 21, 23, 24, 31, 33],
    '发达数':[15,16,24,31,32,33,41,52],
    '温训数':[5,6,11,15,16,24,25,31,32,35,45],
    '女德数':[5,6,15,16,35],
    '荫家数':[3,5,6,11,13,15,16,24,31,32,35],
    '艺能数':[13,14,22,26,29,33,36,38,42],
    '撒娇数':[15,19,24,25,26,32,42]
}

# refer: myself
DAJI_STROKE_TYPES = {
    'male':['首领数', '发达数'],
    'female':['']
}

def bagua_wuxing(stroke_num):
    wuxing_stroke = stroke_num % 10
    if wuxing_stroke in [3, 8]:
        return '木'
    if wuxing_stroke in [2, 7]:
        return '火'
    if wuxing_stroke in [5, 0]:
        return '土'
    if wuxing_stroke in [4, 9]:
        return '金'
    if wuxing_stroke in [1, 6]:
        return '水'

def tian_ge(xing, bihua):
    if len(xing) == 1:
        return bihua[xing[0]] + 1
    if len(xing) == 2:
        return sum([bihua[x] for x in xing])

    raise Exception('unknown xing:{}'.format(xing))

def di_ge(ming, bihua, wanted_num=None):
    if wanted_num is None:
        return sum([bihua[x] for x in ming])
    return wanted_num - ming[0]

def ren_ge(xing, ming, bihua, wanted_num=None):
    if wanted_num is None:
        return bihua[xing[-1]] + bihua[ming[0]]
    return wanted_num - xing[-1]

def ge(xing, ming, bihua):
    return tian_ge(xing, bihua), ren_ge(xing, ming, bihua), di_ge(ming, bihua)

def wuge_wuxing_filter(xing, ming, wuxing):
    pass

if __name__ == '__main__':
    sex = 'male'
    #book_file = 'books/chuci.txt'
    #book_file = 'books/all.txt'
    book_file = 'books/shijing.txt'
    daji_stroke_num = []
    for t in DAJI_STROKE_TYPES[sex]:
        daji_strokes = DAJI_STROKE_NUMBER[t]
        print(t, daji_strokes)
        daji_stroke_num = daji_stroke_num + daji_strokes
    daji_stroke_num = (sorted(list(set(daji_stroke_num))))
    ren_ge_strokes = []
    for daji in daji_stroke_num:
        ren_ge_stroke = ren_ge(xing=[5], ming=None, bihua=None, wanted_num=daji)
        if ren_ge_stroke < 1:
            continue
        ren_ge_strokes.append(ren_ge_stroke)

    res_strokes = []
    for ren_ge_stroke in ren_ge_strokes:
        for daji in daji_stroke_num:
            if daji <= ren_ge_stroke:
                continue
            di_ge_stroke = di_ge(ming=[ren_ge_stroke], wanted_num=daji, bihua=None)
            res_strokes.append([ren_ge_stroke, di_ge_stroke])

    for stroke in res_strokes:
        wd1, wd2 = stroke
        stroke_name_file = '{wd1}_{wd2}.name'.format(wd1=wd1, wd2=wd2)
        if not os.path.isfile(stroke_name_file):
            cmd = 'python naming.py tid3_wd{wd1}.agg tid3_wd{wd2}.agg > {output_file}'.format(wd1=wd1, wd2=wd2,
                    output_file=stroke_name_file)
            ret = subprocess.check_call(cmd, shell=True)
            if ret != 0:
                print('gen name by stroke failed:', stroke)
                sys.exit(1)
        else:
            print(stroke_name_file, ' exists')

        cmd = 'python meaning_filter.py {name_file} {book_file}'.format(name_file=stroke_name_file,
        book_file=book_file)
        ret = subprocess.check_call(cmd, shell=True)
        if ret != 0:
            print('fileter name by book filed:', stroke_name_file, book_file)
            sys.exit(2)


