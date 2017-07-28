#!/usr/bin/env python
# -*- coding: utf-8 -*-

# palindrome is a number like 1221 12321, from start or end with same order
# then 1234 is not a palindrome cause 1=>4 not the same

def is_palindrome(n):
    n = str(n)
    l = len(n)
    s = 0
    e = l - 1
    res = True
    while s < e:
        if n[s] != n[e]:
            res = False
            break
        s += 1
        e -= 1
    return res


def doJob():
    l = list(filter(is_palindrome, range(100, 1000)))
    print(l)


doJob()

