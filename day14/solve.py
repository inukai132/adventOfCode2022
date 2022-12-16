from pprint import pprint
from collections import deque

def get(map, x,y):
  return map[y][x]


def sandFall(map, x, y):
  res = None
  #print()
  #print('\n'.join(map))
  #if y >= 199:
  #  return (x,200)
  if y<0:
    return False
  if x<1 or x>MAP_WIDTH-2:
    raise Exception("MAP_WIDTH too small!")
  if get(map, x, y) in ["#","o"]:
    return False
  if get(map,x,y+1) in ["."]:         #try down
    res = sandFall(map,x,y+1)
  if not res:                             #then left
    res = sandFall(map, x-1, y + 1)
  if not res:                             #then right
    res = sandFall(map, x+1, y + 1)
  if res:
    return res
  return (x,y)



def dropSand(map):
  cur = [SAND_START[0],SAND_START[1]]
  while cur[1] < 200:

    cur[1] += 1
    off = 0

def addSand(map,x,y):
  map[y] = map[y][:x] + "o" + map[y][x + 1:]
  return map


if __name__ == '__main__':
  ins = open('input.txt').read().strip().split('\n')
  ins_ = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''.split('\n')

  MAP_WIDTH = 600
  X_OFFSET = 200
  SAND_START = (500-X_OFFSET,0)
  map = []          #X: 200-800, Y:0-200
  height = 0
  for _ in range(200):
    map.append('.'*MAP_WIDTH)
  for line in ins:
    pts = []
    for p in line.split(' -> '):
      x,y = p.split(',')
      x = int(x)-X_OFFSET
      y = int(y)
      pts.append((x,y))
      if y > height:
        height = y+1
    for i in range(0, len(pts)-1):
      dx = 1 if pts[i+1][0]-pts[i][0] > 0 else -1 if pts[i+1][0]-pts[i][0] < 0 else 0
      dy = 1 if pts[i+1][1]-pts[i][1] > 0 else -1 if pts[i+1][1]-pts[i][1] < 0 else 0

      cur = [pts[i][0], pts[i][1]]
      while cur[0] != pts[i+1][0] or cur[1] != pts[i+1][1]:
        map[cur[1]] = map[cur[1]][:cur[0]] + "#" + map[cur[1]][cur[0]+1:]
        cur[0] += dx
        cur[1] += dy
        map[cur[1]] = map[cur[1]][:cur[0]] + "#" + map[cur[1]][cur[0]+1:]
  map = map[:height]
  map[0] = map[0][:SAND_START[0]] + "+" + map[0][SAND_START[0]+1:]
  map.append('.'*MAP_WIDTH)
  map.append('#'*MAP_WIDTH)
  new = sandFall(map, SAND_START[0], SAND_START[1])
  sands = 0
  #while new[1] < 200:
  #  sands += 1
  #  map = addSand(map,new[0], new[1])
  #  new = sandFall(map, SAND_START[0], SAND_START[1])
  print(sands)
  while new != SAND_START:
    sands += 1
    map = addSand(map,new[0], new[1])
    new = sandFall(map, SAND_START[0], SAND_START[1])
    if sands % 5000 == 0:
      print('\n' + '\n'.join(map))
  sands += 1
  map = addSand(map, new[0], new[1])
  print('\n'+'\n'.join(map))
  print(sands)
