from pprint import pprint
from collections import deque

HEIGHT = 5

def testCollision(board, rock, dir):
  newX, newY = rock.tryMove(dir)


class Board:
  def __init__(self, width):
    self.field = [ ' '*7 for _ in range(HEIGHT+3) ]
    self.rock = None
    self.spawnX = 2
    self.spawnY = len(self.field)-3
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
    for i,l in enumerate(self.field):
      if '#' in l:
        while abs(self.getHeight()-len(self.field)) < 5:
          self.field = [' '*self.width]+self.field
        self.spawnY = i-3
        break

    self.rock = None
    self.settled = True



  def addRock(self, pattern):
    assert(self.settled)
    r = Rock(pattern,self.spawnX,self.spawnY)

    self.rock = r
    self.settled = False

  def getHeight(self):
    return self.height+sum(['#' in l for l in self.field])

  def __repr__(self):
    if len(self.field) > 50:
      return "Field too big to display..."
    f = self.field.copy()
    if self.rock:
      p = self.rock.pattern.split('\n')
      for y in range(self.rock.height):
        for x in range(self.rock.width):
          if p[y][x] == '#':
            f[self.rock.y+y] =f[self.rock.y+y][:self.rock.x+x]+'@'+f[self.rock.y+y][self.rock.x+x+1:]
    return '\n'.join(['|'+x+'|' for x in f]+['+-------+'])


class Rock:
  def __init__(self, pattern, x, y):
    self.pattern = pattern
    self.height = len(pattern.split('\n'))
    self.width = len(pattern.split('\n')[0])
    self.x = x
    self.y = y-self.height


  def tryMove(self,dir):
    match dir:
      case '<':
        return (self.x-1, self.y)
      case '>':
        return (self.x+1, self.y)
      case 'V':
        return (self.x, self.y+1)



if __name__ == '__main__':

  rocks = ['####',' # \n###\n # ','  #\n  #\n###','#\n#\n#\n#','##\n##']

  WIDTH=7

  ins = open('input.txt').read().strip()
  ins = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''

  b = Board(WIDTH)
  fallStep = False
  #for r_ in range(1000000000000+1):
  for r_ in range(2022+1):
    rock_i = r_%len(rocks)
    fallStep = False
    pattern = rocks[rock_i]
    b.addRock(pattern)
    rock = b.rock
    l = rock.x
    r = rock.x+rock.width
    Xshift = 0
    Yshift = 3
    for c in ins[:4]:
      if c == '<' and l+Xshift == 0:
        continue
      if c == '>' and r+Xshift == 7:
        continue
      Xshift += 1 if c == '>' else -1
    fallStep = True
    rock.x += Xshift
    rock.y += Yshift
    ins = ins[4:]+ins[:4]
    #print(b)
    print(f"{b.getHeight()+b.height} - {r_}")
    if b.getHeight() < 50:
      print(b)
    while not b.settled:
      if not fallStep:
        b.step(ins[0])
        l=len(ins)
        ins = ins[1:]+ins[0]
        assert(l==len(ins))
      else:
        b.step('V')
      fallStep = not fallStep
