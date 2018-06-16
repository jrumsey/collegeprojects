import random
import math

#array = [];
array = [10, 9, 8, 7, 6, 1, 4, 3, 2, 5]

def quicksort1(low, high): 
  if(high > low):
    pivotpoint = 5 
    partition(low, high, pivotpoint)
    print array
#    quicksort1(low, pivotpoint - 1)
#    quicksort1(pivotpoint + 1, high)


def partition(low, high, pivotpoint):
  
  pivotitem = array[low]
  j = low
  i = low + 1

#  for index in range(i, high):
  while(i <= high):
    if(array[i] < pivotitem):
      j = j + 1
      temp = array[i]
      array[i] = array[j]
      array[j] = temp
    i = i + 1
 
  pivotpoint = j
  temp = array[low]
  array[low] = array[pivotpoint]
  array[pivotpoint] = temp

  

#main

print "Randomized array: "

for i in range(0, 10):
  randnum = random.randint(0, 20)
#  array.append(randnum)
print array
  
print "Sorted array: "

quicksort1(0, len(array) - 1)

print array


