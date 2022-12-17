from pprint import pprint
from collections import deque

HEIGHT = 5

def testCollision(board, rock, dir):
  newX, newY = rock.tryMove(dir)


class Board:
  def __init__(self, width):
    self.field = [ ' '*width for _ in range(0) ]
    self.rock = None
    self.spawnX = 2
    self.spawnY = len(self.field)-4
    self.width = width
    self.settled = True
    self.height = 0

  def pointOccupied(self,x,y):
    return self.field[y][x] in '#@'

  def step(self,dir):
    newX, newY = self.rock.tryMove(dir)
    if newY+self.rock.height > len(self.field):
      self.settle()
      return
    if newX < 0 or newX+self.rock.width > self.width:
      return

    p = self.rock.pattern.split('\n')
    for y in range(self.rock.height):
      for x in range(self.rock.width):
        if p[y][x] == '#' and self.pointOccupied(x+newX,y+newY):
          if newY > self.rock.y:
            self.settle()
            return
          return
    self.rock.x = newX
    self.rock.y = newY
    return

  def settle(self):
    for y in range(self.rock.height):
      for x in range(self.rock.width):
        p = self.rock.pattern.split('\n')
        if p[y][x] == '#':
          self.field[self.rock.y+y] = self.field[self.rock.y+y][:self.rock.x+x]+'#'+self.field[self.rock.y+y][self.rock.x+x+1:]
    if '#'*7 in self.field:
      newFloor = self.field.index('#'*7)
      self.height += len(self.field) - newFloor
      self.field = self.field[:newFloor]

    self.rock = None
    self.settled = True



  def addRock(self, pattern):
    assert(self.settled)
    for i,l in enumerate(self.field):
      if '#' in l:
        self.spawnY = (i-4)
        break
    while (self.spawnY) - len(pattern.split('\n')) < -1:
      self.field = [' '*self.width]+self.field
      self.spawnY += 1
    r = Rock(pattern,self.spawnX,self.spawnY)

    self.rock = r
    self.settled = False

  def getHeight(self):
    return self.height+sum(['#' in l for l in self.field])

  def simplify(self):
    newFloor = 0
    while self.field[0] == ' '*7:
      self.field = self.field[1:]
      self.spawnY -= 1
    for x in range(self.width):
      for i,row in enumerate(self.field):
        if row[x] == '#':
          newFloor = max(newFloor,i)
          break
        return
    self.height += len(self.field)-newFloor
    self.field = self.field[:newFloor]

  def __repr__(self, force = False):
    if len(self.field) > 50 and not force:
      return "Field too big to display..."
    f = self.field.copy()
    if self.rock:
      p = self.rock.pattern.split('\n')
      for y in range(self.rock.height):
        for x in range(self.rock.width):
          if p[y][x] == '#':
            f[self.rock.y+y] =f[self.rock.y+y][:self.rock.x+x]+'@'+f[self.rock.y+y][self.rock.x+x+1:]
    return '\n'.join(['|'+x+'|' for x in f]+['+-------+']).replace(' ','.')+'\n'


class Rock:
  def __init__(self, pattern, x, y):
    self.pattern = pattern
    self.height = len(pattern.split('\n'))
    self.width = len(pattern.split('\n')[0])
    self.x = x
    self.y = y-self.height+1


  def tryMove(self,dir):
    match dir:
      case '<':
        return (self.x-1, self.y)
      case '>':
        return (self.x+1, self.y)
      case 'V':
        return (self.x, self.y+1)


def dropRock(r_):
  global  ins, b
  rock_i = r_ % len(rocks)
  fallStep = False
  pattern = rocks[rock_i]
  b.addRock(pattern)
  # if debug:
  #  print(b)
  rock = b.rock
  l = rock.x
  r = rock.x + rock.width - 1
  Xshift = 0
  Yshift = 3
  for c in ins[:4]:
    if c == '<' and l + Xshift == 0:
      continue
    if c == '>' and r + Xshift == 6:
      continue
    Xshift += 1 if c == '>' else -1
  fallStep = True
  rock.x += Xshift
  rock.y += Yshift
  ins = ins[4:] + ins[:4]
  # if debug:
  #  print(b)
  # if r_ % 10000 == 0:
  #  print(f"{b.getHeight()+b.height} - {r_}")
  while not b.settled:
    if not fallStep:
      b.step(ins[0])
      l = len(ins)
      ins = ins[1:] + ins[0]
      assert (l == len(ins))
    else:
      b.step('V')
    fallStep = not fallStep
    # if debug:
    #  print(b)


if __name__ == '__main__':

  rocks = ['####',' # \n###\n # ','  #\n  #\n###','#\n#\n#\n#','##\n##']

  WIDTH=7

  ins = open('input.txt').read().strip()
  ins = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''

  b = Board(WIDTH)
  fallStep = False
  p1 = True
  iter = 2022+1 if p1 else 1000000000000+1
  floorCycleLen = 7 if len(ins) < 100 else 242
  cycleLen = len(ins)*len(rocks)
  print(cycleLen)
  floors = []
  heights = []
  lastHeight = 0
  for r_ in range(floorCycleLen*cycleLen):
    dropRock(r_)
    b.simplify()
  for r_ in range(floorCycleLen * cycleLen):
    if len(floors) != floorCycleLen:
      floors.append(b.field)
    heights.append(b.getHeight()-lastHeight)
    lastHeight = b.getHeight()
    print(r_,heights[-1])

  quit(0)
  lastHeight = 0

  for i in range(floorCycleLen):
    for r_ in range(cycleLen):
      dropRock(r_+1)
    b.simplify()
    #print(b)
    f = b.field.copy()
    if f not in floors:
      print("Floor not in results")
    else:
      print(F"Found floor {floors.index(f)}")
    floors.append(f)
    heights.append(b.getHeight()-lastHeight)
    print(f"Height: {b.getHeight()}")
  print(len(floors))






  quit(0)
  finalFloor = floors[iter // floorCycleLen]
  for r_ in range(iter%floorCycleLen):
    rock_i = r_ % len(rocks)
    fallStep = False
    pattern = rocks[rock_i]
    b.addRock(pattern)
    # if debug:
    #  print(b)
    rock = b.rock
    l = rock.x
    r = rock.x + rock.width - 1
    Xshift = 0
    Yshift = 3
    for c in ins[:4]:
      if c == '<' and l + Xshift == 0:
        continue
      if c == '>' and r + Xshift == 6:
        continue
      Xshift += 1 if c == '>' else -1
    fallStep = True
    rock.x += Xshift
    rock.y += Yshift
    ins = ins[4:] + ins[:4]
    # if debug:
    #  print(b)
    # if r_ % 10000 == 0:
    #  print(f"{b.getHeight()+b.height} - {r_}")
    while not b.settled:
      if not fallStep:
        b.step(ins[0])
        l = len(ins)
        ins = ins[1:] + ins[0]
        assert (l == len(ins))
      else:
        b.step('V')
      fallStep = not fallStep
      # if debug:
      #  print(b)
  b.simplify()
