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
    for i,l in enumerate(self.field):
      if '#' in l:
        while abs(self.getHeight()-len(self.field)) < 10:
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
    return sum(['#' in l for l in self.field])

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
  ins_i = 0
  for r in range(2023):
    rock_i = r%len(rocks)
    pattern = rocks[rock_i]
    b.addRock(pattern)
    #print(b)
    print(b.getHeight())
    while not b.settled:
      if (ins_i & 1) == 0:
        b.step(ins[ins_i//2])
      else:
        b.step('V')
      #print(b)
      #print(b.getHeight())
      ins_i += 1
      ins_i %= len(ins)*2
