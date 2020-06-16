import sys
from itertools import product
from kx_word_extract import load_checkpoint

def load_word(word_file):
    word_records = {}
    try:
        with open(word_file) as f:
            for line in f:
                w, v = line.strip().split(',')
                word_records[w] = v
    except:
        print('file not found:{}'.format(output_file))
    return word_records

def combine(words, combine_method='cross'):
    combinations = []
    for comb in product(*words):
        combinations.append(comb)
    return combinations

def filter_name(names, condition):
    res_names = []
    for name in names:
        w1, w2 = name
        if condition(w1, w2):
            res_names.append((w1, w2))
    return res_names

def filter_char(ws, condition):
    res_w = {}
    for w in ws.items():
        if condition(w):
            k, v = w
            res_w.update({k:v})
    return res_w

def wuxing_in(w1, w2):
    global word_info
    global wuxing_range
    wx1 = word_info[w1]
    wx2 = word_info[w2]
    if wx1 in wuxing_range or wx2 in wuxing_range:
        #print(w1, wx1, w2, wx2, wuxing_range)
        return True
    return False

def wuxing_not_in(w1, w2):
    global word_info
    global wuxing_not_in_range
    wx1 = word_info[w1]
    wx2 = word_info[w2]
    if wx1 in wuxing_not_in_range or wx2 in wuxing_not_in_range:
        return False
    return True

def w1_in(w1):
    global word_info
    global w1_range
    k, v = w1
    #print('w1_range:', w1_range, k)
    if k in w1_range:
        return True
    return False


if __name__ == '__main__':
    file1, file2 = sys.argv[1], sys.argv[2]
    w1 = load_word(file1)
    w2 = load_word(file2)
    word_info = {}
    word_info.update(w1)
    word_info.update(w2)
    #w1_range = ['一', '乙']
    #w1 = filter_char(w1, w1_in)
    #print(w1)
    names = combine([w1.keys(), w2.keys()])
    print('combined:',len(names))
    wuxing_range = ['(土)']
    wuxing_not_in_range = []
    names = filter_name(names, wuxing_in)
    print('wuxing_in:',len(names))
    names = filter_name(names, wuxing_not_in)
    print('wuxing_not_in:',len(names))
    for n in names:
        w1, w2 = n
        wx1, wx2 = word_info[w1], word_info[w2]
        print(w1, wx1, w2, wx2)
