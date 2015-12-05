#!/usr/local/bin/python3

import hashlib


def md5_hash(string):
    h = hashlib.md5()
    h.update(string.encode())
    return h.hexdigest()


md5_key = 'ckczppom'
for prefix in ['0' * 5, '0' * 6]:
    num = 1
    while True:
        result = md5_hash(md5_key + str(num))
        if result.startswith(prefix):
            print(num, result)
            break
        num += 1
