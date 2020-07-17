import sys
import os
import re
import time
import random
import subprocess


def parse_file(file_name):
    output_words = []
    with open(file_name) as f:
        for line in f:
            RE = re.compile(r'.*<span class="sotab_zi_l">(.*?)</span>.*<span class="sotab_zi_r"> (.*?)</span>.*', re.I|re.U)
            m = RE.match(line)
            if m is None:
                continue
            FINDRE = re.compile(r'<span class="sotab_zi_l">(.*?)</span> <span class="sotab_zi_r"> (.*?)</span>', re.I|re.U)
            m = FINDRE.finditer(line)
            for v in m:
                sub_wd = v.group()
                EXTRE = re.compile(r'<span class="sotab_zi_l">(.*?)</span> <span class="sotab_zi_r"> (.*?)</span>', re.I|re.U)
                m = EXTRE.match(sub_wd)
                w, v = m.groups()
                output_words.append((sub_wd, w, v))
    return output_words


def download(wd=1, tid=3, page_index=0, outpath='./tmp/'):
    output_file = '{}/tid{}_wd{}_page{}.txt'.format(outpath, tid, wd, page_index)
    cmd = 'curl -v "http://tool.httpcn.com/KangXi/So.asp?Tid={tid}&wd={wd}" > {output}'.format(tid=tid, wd=wd, output=output_file)
    print(cmd)
    ret = subprocess.check_call(cmd, shell=True)
    if ret != 0:
        print('download failed')
        return False
    print('download ok to {}'.format(output_file))
    return output_file


def parse(file_name, append_file_name):
    parsed_words = parse_file(file_name)
    word_map = {}
    with open(append_file_name, 'a') as f:
        for _, w, v in parsed_words:
            word_map[w] = v
            f.write(','.join([w, v]) + '\n')
    return word_map


def load_checkpoint(output_file, download_path, tid, word_count):
    word_records = {}
    try:
        with open(output_file) as f:
            for line in f:
                w, v = line.split(',')
                word_records[w] = v
    except:
        print('file not found:{}'.format(output_file))
    page_index = 0
    for f in [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]:
       want_prefix = 'tid{}_wd{}_'.format(tid, word_count)
       if want_prefix not in f:
           continue
       page_str = (f.split('.')[0]).split('_')[2]
       cur_page_index = int(page_str.replace('page',''))
       if cur_page_index > page_index:
           page_index = cur_page_index
    return word_records, page_index


if __name__ == '__main__':
    word_record = {}
    tid = 3
    word_count = int(sys.argv[1])
    page_index = 0
    last_wd_size = -1
    word_output_file = 'tid{}_wd{}.agg'.format(tid, word_count)
    outpath = './tmp'
    word_record, page_index = load_checkpoint(word_output_file, outpath, tid, word_count)
    print('load info word:{} page index:{}'.format(len(word_record), page_index))
    while last_wd_size != len(word_record):
        last_wd_size = len(word_record)
        download_file = download(wd=word_count, tid=tid, page_index=page_index, outpath=outpath)
        parsed_word = parse(download_file, word_output_file)
        page_index = page_index + 1
        word_record.update(parsed_word)
        sleep_sec = random.randint(3, 5)
        print('sleep sec:', sleep_sec, len(word_record))
        time.sleep(sleep_sec)

