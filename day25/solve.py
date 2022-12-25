import queue
from pprint import pprint
from collections import deque
import math

def snaf2dec(s):
  d = 0
  numerals = '=-012'
  place = 1
  for c in s[::-1]:
    d += (numerals.index(c)-2)*place
    place *= 5
  return d

def dec2snaf(d):
  #Convert to base5
  b5 = []
  while(d):
    b5 = [d%5] + b5
    d //= 5
  for i in range(len(b5)-1,0,-1):
    if b5[i] > 4:
      b5[i-1] += 1
      b5[i] %= 5

    if b5[i] == 3:
      b5[i-1] += 1
      b5[i] = -2

    if b5[i] == 4:
      b5[i-1] += 1
      b5[i] = -1

  return ''.join(['=-012'[i+2] for i in b5])


def aStar(target):
  curPos = ''
  maxLen = math.log(target,2)+1
  frontier = queue.PriorityQueue()
  frontier.put((0,curPos))
  visited = []
  moves = '0=-12'[::-1]
  minDif = target
  while not frontier.empty():
    pri, step = frontier.get()
    if len(step) > maxLen:
      continue
    for move in moves:
      newPos = step+move
      if newPos in visited:
        continue
      visited.append(newPos)
      newInt = snaf2dec(newPos)
      dif = target - newInt
      if dif < 0:
        continue
      if dif < minDif:
        print(dif)
        minDif = dif
      if dif == 0:
        print('*'*80+'/n'+newPos+'/n'+'*'*80)
        return newPos
      frontier.put((dif+(len(newPos)),newPos))



if __name__ == '__main__':
  ins = open('input.txt').read().split('\n')
  ins_ = '''1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122'''.split('\n')

  d = sum([snaf2dec(l) for l in ins])
  print(dec2snaf(d))

