#!/usr/bin/env python
# -*- coding: utf-8 -*-

age = input('pleas input your age: ')
age = int(age)
school=None
if age < 12 and age >= 6:
    school = 'primary'
elif age >= 12 and age < 15:
    school = 'junior'
elif age >= 15 and age < 18:
    school = 'high'
elif age >= 18:
    school = 'collage'
else:
    school = 'no'
            
print('age = %d, can go to %s school' % (age, school))
