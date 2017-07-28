#!/usr/bin/env python
# -*- coding: utf-8 -*-

# decrator the function to add some power

def log(func):
    def wrapper(*args, **kw):
        print('call %s()' % func.__name__)
        return func(*args, **kw)
    return wrapper


@log
def now(time):
    print('2017-07-28 %s' % time)

now('13:25:11')
