from functools import cache
from pprint import pprint
from collections import deque

def adj(a,b):
  #Adjacent if exactly one dim is exactly one unit away
  comps = [a[i]==b[i] for i in range(3)]
  dimsEq = sum(comps)
  if dimsEq != 2:
    return False
  for i,c in enumerate(comps):
    if not c:
      return abs(a[i]-b[i]) == 1

freeBlocks = []

def dfs(a,b,walls,minD,maxD,visited=[]):
  global freeBlocks
  dirs = (
    (0,0,-1),
    (0,0,1),
    (-1,0,0),
    (1,0,0),
    (0,-1,0),
    (0,1,0),
  )

  if a in freeBlocks:
    return True

  if a==b:
    if a not in walls:
      freeBlocks.append(a)
    return True
  if a in walls or a in visited:
    return False
  visited.append(a)
  for d in dirs:
    a_ = [a[i]+d[i] for i in range(3)]
    if any([x>maxD or x<minD for x in a_]):
      continue
    if dfs(a_,b,walls,minD,maxD,visited):
      if a not in walls:
        freeBlocks.append(a)
      return True
  return False

def dist(a,b):
  dst = pow(a[0]-b[0],2)
  dst += pow(a[1]-b[1],2)
  dst += pow(a[2]-b[2],2)
  return pow(dst,.5)

if __name__ == '__main__':
  ins = open('input.txt').read().split('\n')
  ins_ = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''.split('\n')
  cubes = []
  for line in ins:
    cubes.append([int(a) for a in line.split(',')])
  area = 0
  for cube in cubes:
    area+=6
    area -= sum([adj(cube,a) for a in cubes])
  print(area)

  import sys

  sys.setrecursionlimit(20*20*20)

  minD = min([min(a) for a in cubes])-1
  maxD = max([max(a) for a in cubes])+1
  print(f"Search from {minD} to {maxD}")
  minP = [minD, minD, minD]
  maxP = [maxD, maxD, maxD]
  for x in range(minD,maxD):
    for y in range(minD,maxD):
      print(x,y,len(freeBlocks))
      for z in range(minD,maxD):
        p = [x,y,z]
        tgt = minP
        if dist(p,minP) > dist(p,maxP):
          tgt = maxP
        if not dfs(p, tgt, cubes, minD, maxD, []) and p not in cubes:
          area -= sum([adj(p,a) for a in cubes])

  print(area)