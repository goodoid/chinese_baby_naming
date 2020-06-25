import sys
import os
import re
import time
import random
import subprocess


if __name__ == "__main__":
    named_file = sys.argv[1]
    book_file = sys.argv[2]
    words = []
    with open(named_file) as f:
        for line in f:
            l = line.split()
            if len(l) != 4:
                continue
            words.append([l[0], l[2]])
    print('named_file:{} book_file:{} name count:{}'.format(named_file, book_file, len(words)))
    book_lines = []
    with open(book_file) as f:
        for line in f:
            if line.strip():
                book_lines.append(line)

    print('book lines:{}'.format(len(book_lines)))
    for word in words:
        w1, w2 = word
        for line in book_lines:
            RE=re.compile(r'.*{}[^，。]?{}.*'.format(w1, w2), re.U)
            m = RE.match(line)
            if m is None:
                continue
            print(word, line)

