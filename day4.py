#!/usr/local/bin/python3

import hashlib

md5_key = 'ckczppom'

num = 1


def md5_hash(key, number):
    h = hashlib.md5()
    string = md5_key + str(num)
    h.update(string.encode())
    return h.hexdigest()


for prefix in ['0' * 5, '0' * 6]:
    while True:
        result = md5_hash(md5_key, num)
        if result.startswith(prefix):
            print(num, result)
            break
        num += 1
