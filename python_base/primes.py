#!/usr/bin/env python
# -*- coding: utf-8 -*-

## according to aishi filter to find all primes nums from 1~1000
## for example: n = 2 3 4 5 6 7 8 9
## first, 2 is an primes, then filter n with 2k(k=2,3,4...),then n = 2 3 5 7 9
## then next one is 3, is also an primes, can filter its times, then = 2 3 5 7
## then next is 5, is an primes, do the same and so on. the result is 2 3 5 7

def primes():
    yield 2
    generator = odd_iter()
    while True:
        n = next(generator)
        yield n
        generator = filter(not_dividable(n), generator)

def odd_iter():
    n = 1
    while True:
        n += 2
        yield n


def not_dividable(n):
    return lambda x: x % n > 0


def doJob():
    for n in primes():
        if (n < 100):
            print(n, ' ')
        else:
            break

# do the job
doJob()
