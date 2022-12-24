from pprint import pprint
from collections import deque

def printBoard(elves):
  nx = min([e[0] for e in elves])
  px = max([e[0] for e in elves])
  ny = min([e[1] for e in elves])
  py = max([e[1] for e in elves])
  board = ['.'*(px-nx+1) for _ in range(py-ny+1)]
  for x,y in elves:
    board[y-ny] = board[y-ny][:x-nx]+'#'+board[y-ny][x+1-nx:]
  print('\n'.join(board))
  return board

def moveElf(ins):
  elf, elves, dirs = ins
  found = False
  for dx in range(-1, 2):
    for dy in range(-1, 2):
      if dx == 0 and dy == 0:
        continue
      if [elf[0] + dx, elf[1] + dy] in elves:
        found = True
  if not found:
    return elf

  done = False
  for dir in dirs:
    found = False
    for n in range(-1, 2):
      searchSpot = [dir[0], dir[1]]
      searchIdx = dir.index(0)
      searchSpot[searchIdx] = n
      searchSpot = [searchSpot[i] + elf[i] for i in range(2)]
      if searchSpot in elves:
        found = True
        break
    if not found:
      newSpot = [elf[i] + dir[i] for i in range(2)]
      return newSpot
  return elf

if __name__ == '__main__':
  ins = open('input.txt').read().strip().split('\n')
  ins1 = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..'''.split('\n')
  ins2 = '''.....
..##.
..#..
.....
..##.
.....'''.split('\n')

  elves = []
  for y,row in enumerate(ins):
    for x,cell in enumerate(row):
      if cell == '#':
        elves.append([x,y])

  dirs = deque([(0,-1),(0,1),(-1,0),(1,0)])
  b = printBoard(elves)
  print(-1)
  print()

  r = 1
  from multiprocessing import Pool
  p = Pool()
  while True:
    props = p.map(moveElf, [(elf, elves, dirs) for elf in elves])

    assert(len(props) == len(elves))

    elfMoved = False
    for i,newSpot in enumerate(props):
      if props.count(newSpot) > 1:
        continue
      else:
        if not elfMoved and elves[i] != newSpot:
          elfMoved = True
        elves[i] = newSpot
    if not elfMoved:
      print('*'*20)
      print(r)
      print('*'*20)
      open('done','w').write(str(r))
      break
    print(r)
    open('debug','w').write(str(r))
    r+=1
    dirs.rotate(-1)