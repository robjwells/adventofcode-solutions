#!/usr/local/bin/python3

import hashlib

md5_key = 'ckczppom'
for prefix in ['0' * 5, '0' * 6]:
    num = 1
    while True:
        string = md5_key + str(num)
        result = hashlib.md5(string.encode()).hexdigest()
        if result.startswith(prefix):
            print(num, result)
            break
        num += 1
