#!/usr/bin/env python
# -*- coding: utf-8 -*-

list1 = [1,2,3,4]
print(list1, ', length=%d' % len(list1))
list1.append('cx')
list1.insert(0,'haha')
list1.pop(1)
print('list can be changed by append, insert, pop, now it\'s', list1, 'lenth=%d' % len(list1))

tuple1 = (1,2,3,4)
print('''tuple can\'t change its point to the element, 
but it\'s much safer than array,''',
     tuple1, 'length = %d ' % len(tuple1))
t0 = (1,2,[3,4])
t0[-1].append(5)
print('with list element in tuple, it\'s ok to change list\'s elements', t0)


t1 = ('sss')
print('only one element for tuple is (\'sss\',), or it will be computed %s'% t1)

