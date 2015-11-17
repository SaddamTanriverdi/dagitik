import numpy
import random
import scipy.stats

a1 = numpy.random.normal(-5,1.5,10000)
a2 = numpy.random.normal(5,1.4,10000)

for i in range(10000):
   a1[i] = round(a1[i])
   a2[i] = round(a2[i])

'''Histogram olusturma'''
l1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
l2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

c = -20
d = 0
for i in range(10000):
    for c in range(-20,21):
        if a1[i] == c:
            l1[d] = l1[d] + 1            
        if a2[i] == c:
            l2[d] = l2[d] + 1   
        c = c + 1
        d = d + 1
    c = -20
    d = 0

'''Normalize edilmis hal '''
for i in range(41):
    l1[i] = (l1[i]/10000)
    l2[i] = (l2[i]/10000)

print(l1)
print(l2)

'''Distance hesaplama'''
l3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
m2 = [-20, -19, -18, -17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
m1 = [-20, -19, -18, -17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

k = 0
distance = 0

for a in range(41):
   if l2[a] != 0:
    for b in range(41):
        if l1[b] != 0:
            if l2[a] == l1[b]:
                l1[b] = 0
                l3[a] = l1[b] 
                k = abs(m2[a]-m1[b])
                distance = distance + (k * l1[b])
            elif l2[a] > l1[b]:
                l3[a] = l1[b]
                l2[a] = l2[a] - l1[b]
                k = abs(m2[a]-m1[b])
                distance = distance + (k * l1[b])
                l1[b] = 0
            elif l2[a] < l1[b]:
                l3[a] = l2[a]
                l1[b] = l1[b] - l2[a]
                k = abs(m2[a]-m1[b])
                distance = distance + (k * l2[a])
                l2[a] = 0
print(l3)             
print(distance)
