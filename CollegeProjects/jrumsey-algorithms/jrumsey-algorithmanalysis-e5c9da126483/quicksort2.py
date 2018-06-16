import random

array = [];

def quicksort2(low, high):
  pivotpoint = low 

  if(high > low):
    partition(low, high, pivotpoint)
    quicksort2(low, pivotpoint - 1)
    quicksort2(pivotpoint + 1, high)

def partition(low, high, pivotpoint):
  pivotitem = array[low]
  i = low
  j = high

  while(i < high and array[i] <= pivotitem):
    i = i + 1
  while(array[j] > pivotitem):
    j = j - 1
  while(i < j):
    temp = array[i]
    array[i] = array[j]
    array[j] = array[i]
    while(array[i] <= pivotitem):
      i = i + 1
    while(array[j] > pivotitem):
      j = j - 1
  pivotpoint = j
  temp = array[low]
  array[low] = array[pivotpoint]
  array[pivotpoint] = temp

#main

print "Randomized array: "

for i in range(0, 10):
 randnum = random.randint(0, 20)
 array.append(randnum)

print array

print "Sorted array: "

quicksort2(0, 9)

print array
