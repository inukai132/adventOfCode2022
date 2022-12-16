from pprint import pprint
from collections import deque

def bfs(start):
  ins = open('input.txt').read().replace('S','a').replace('E','{').split('\n')[:-1]
  que = deque()
  visited = []
  que.append((start,0))
  distance = 0
  visited.append(start)
  while(len(que)):
    cur, dist = que.popleft()
    if ins[cur[1]][cur[0]] == '{':
      return dist
    dist += 1
    visited.append(cur)
    for dir in [(1,0),(0,1),(-1,0),(0,-1)]:
      nextPos = [cur[0]+dir[0],cur[1]+dir[1]]
      if nextPos in visited or nextPos in [a[0] for a in que]:
        continue
      if any(a<0 for a in nextPos) or nextPos[0] >= len(ins[0]) or nextPos[1] >= len(ins):
        continue
      if ord(ins[nextPos[1]][nextPos[0]]) - ord(ins[cur[1]][cur[0]]) > 1:
        continue
      que.append((nextPos,dist))
  return None

if __name__ == '__main__':
  ins = open('input.txt').read().replace('S','`').replace('E','{').split('\n')[:-1]
  ins_ = '''Sabqponm
  abcryxxl
  accszExk
  acctuvwj
  abdefghi'''.replace('S','`').replace('E','{').split('\n')



  start = [-1,-1]
  end = (-1,-1)
  cands = []
  for Y in range(len(ins)):
    for X in range(len(ins[Y])):
      if ins[Y][X] == '`':
        start = [X,Y]
        cands.append([X,Y])
      if ins[Y][X] == '{':
        end = (X, Y)
      if ins[Y][X] == 'a':
        cands.append([X,Y])


  curPos = start
  #out = bfs(curPos)
  #print(out)


  ins = '\n'.join(ins).replace('`','a').split('\n')

  from multiprocessing import Pool

  p = Pool()
  res = p.imap_unordered(bfs,cands)
  print(min([a for a in res if a]))
