#!/usr/bin/env python
# -*- coding: utf-8 -*-

def show(a, b=10,c='cc'):
    print('a=', a, ', b=', b, ', c=', c)
    return 'done'

show(1)
show(1,2)
show(1,c=2) #set the diff arg with its name


def showMore(a,b=10,*num):
    print('a=', a, ', b=', b, ', l=', num)

showMore(1)
showMore(1,11,20,30,40) # args are elements of tuple l and a occupys l[0], b is l[1], the others l[2]~l[n] are num
l = ['a1111', 'b1111']
t = ('z111', 'y111')
showMore(1,11,*l)
showMore(1,11,*t)


def show3(a, b=10, **km):
    print('a=', a, ', b=', b, 'km=', km)

show3(1,2)
show3(1,2,age=10,grade=20) # args are the dict elements
d = {'width': 10, 'height':200}
show3(1,2,**d)


def show4(a, b=10, *, city, name):
   print('a=', a, ', b=', b, ', city=', city, ', name=', name)


#show4(1,city='Shanghai') #missing a required arg named name
#show4(1,city='Shanghai', name='cx', Grade='haha') # got an unexpected arg named Grade
show4(1,city='Shanghai', name='cx')


def show5(a, *num, city='Shanghai', name):
    print('a=', a, ', num=', num, ', city=', city, ', name=', name)

show5(1,20,30,name='cx') # named arg must at the end of a list of args


import logging
def showErr():
   try:
       a = 10 /0
   except Exception as e:
       logging.exception(e)
       print('exception end')


showErr()
