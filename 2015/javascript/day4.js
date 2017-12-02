#!/usr/local/bin/node

'use strict';

var crypto = require('crypto')


var md5_digest = function (string) {
    var hash = crypto.createHash('md5');
    hash.update(string, 'utf-8');
    return hash.digest('hex');
};

var md5_prefix = 'ckczppom';
var num = 1;
['00000', '000000'].forEach(function (prefix) {
   while (true) {
       var digest = md5_digest(md5_prefix + String(num));
       if (digest.startsWith(prefix)) {
           console.log(num, digest);
           break;
       } else {
           num += 1;
       }
   }
});
