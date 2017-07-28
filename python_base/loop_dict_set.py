#!/usr/bin/env python
# -*- coding: utf-8 -*-

a = list(range(5))
for n in a:
    print('list element is: %d' % n)

print('end----------------1')

i = 0
while i < len(a):
    print('the %d th element is: %d' % (i, a[i]))
    i += 1
print('end-----------------2')

d1 = {'a': 'aaa', 'b': 'bb'}
print('dict is a map', d1)
d1['c']='cc'
print('after add one item, it\'s ', d1)

s = set(list(range(5,8)))
print('set is a list of unique values', s, s.add(5), 'after add 5 there is only one 5 ',s)
