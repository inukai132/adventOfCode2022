import math
import queue
from pprint import pprint
from collections import deque


def dist(a,b):
  dx = b[0]-a[0]
  dy = b[1]-a[1]
  return dx**2+dy**2

def bfs(start, end, timeCube, timeStart=0):
  q = queue.PriorityQueue()#deque()
  #q = queue.Queue()#deque()
  visited = []
  curPos = start+[timeStart]
  q.put((dist(curPos,end),[curPos]))
  moves = dirs+[(0,0)]
  min=99999
  while not q.empty():
    pri,path = q.get()
    if pri < min:
      print(pri,len(path)+timeStart)
      min = pri
    node = path[-1]
    if node in visited:
      continue
    visited.append(node)
    for move in moves:
      newPos = [node[i]+move[i] for i in range(2)]+[node[2]+1]
      x,y,t = newPos
      map = timeCube[t%(len(timeCube))]
      if y >= len(map) or x >= len(map[0]) or x < 0 or y < 0:
        continue
      if [x,y] == end:
        print(len(path))
        print(path)
        return path+[newPos]
      if map[y][x] not in 'S.E':
        continue
      if newPos in visited:
        continue
      q.put((dist(newPos,end),path+[newPos]))


def aStar(start, end, timeCube, timeStart=0):
  curPos = start+[timeStart]
  frontier = queue.PriorityQueue()
  frontier.put((0,curPos))
  cameFrom = {}
  costSoFar = {}
  cameFrom[tuple(curPos)] = None
  costSoFar[tuple(curPos)] = 0
  moves = dirs+[(0,0)]
  minT  = 10000000

  while not frontier.empty():
    pri, step = frontier.get()
    if step[2]+1 > minT:
      continue
    for move in moves:
      newPos = [step[i]+move[i] for i in range(2)]+[step[2]+1]
      x,y,t = newPos
      map = timeCube[t%(len(timeCube))]
      if y >= len(map) or x >= len(map[0]) or x < 0 or y < 0:
        continue
      if map[y][x] not in 'S.E':
        continue
      newCost = costSoFar[tuple(step)]+1
      if tuple(newPos) not in costSoFar or newCost < costSoFar[tuple(newPos)]:
        costSoFar[tuple(newPos)] = newCost
        pri = newCost+dist(newPos,end)
        frontier.put((pri,newPos))
        cameFrom[tuple(newPos)] = step
      if [x,y] == end:
        if t < minT:
          print(t)
          minT = t
        #return cameFrom, costSoFar

  return cameFrom, minT


def getStage(bliz, cur=None):
  o = []
  o.append('#'*(maxDim[0]-minDim[0]+2))
  o+=['#'+'.'*(maxDim[0]-minDim[0])+'#' for _ in range(maxDim[1]-minDim[1])]
  o.append('#'*(maxDim[0]-minDim[0]+2))
  for xy,dir in bliz:
    x,y = xy
    c = cDirs[dirs.index(dir)]
    o[y] = o[y][:x]+c+o[y][x+1:]
  o[0] = o[0][:start[0]]+'S'+o[0][start[0]+1:]
  o[-1] = o[-1][:end[0]]+'E'+o[0][end[0]+1:]
  return o

def step(b):
  o = []
  for xy,dir in b:
    x,y = xy
    newX = ((x+dir[0]-1)%width)+1
    newY = ((y+dir[1]-1)%height)+1

    newPos = [[newX,newY],dir]
    o.append(newPos)
  return o

if __name__ == '__main__':
  ins = open('input.txt').read().split('\n')
  ins_ = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''.split('\n')
  ins_ = '''#.######
#......#
#.<v>^.#
#......#
#......#
######.#'''.split('\n')

  dirs = [(1,0),(-1,0),(0,1),(0,-1)]
  cDirs = '><v^'
  start = [ins[0].index('.'),0]
  end = [ins[-1].index('.'),len(ins)-1]
  blizzards = []
  maxDim = (len(ins[0])-1,len(ins)-1)
  minDim = (1,1)
  width = maxDim[0]-minDim[0]
  height = maxDim[1]-minDim[1]
  STEPS=(width*height)//math.gcd(width,height)

  for y,line in enumerate(ins[1:-1]):
    for x,c in enumerate(line):
      if c in cDirs:
        blizzards.append([[x,y+1],dirs[cDirs.index(c)]])

  curPos = [start[0],start[1]]

  print('\n'.join(getStage(blizzards)))
  print("Building time cube")
  timesteps = [getStage(blizzards)]
  for _ in range(STEPS):
    blizzards = step(blizzards)
    timesteps.append(getStage(blizzards))
  assert timesteps[0] == timesteps[-1]
  timesteps = timesteps[:-1]
  print("Running bfs")
  path1,cost1 = aStar(start,end, timesteps)
  print(cost1)
  path2,cost2 = aStar(end,start, timesteps, cost1)
  print(cost2)
  path3,cost3 = aStar(start,end, timesteps, cost2)
  print(cost3)
