import time
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
      found = False
      for i,row in enumerate(self.field):
        if row[x] == '#':
          newFloor = max(newFloor,i)
          found = True
          break
      if not found:
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


def dropRock(b, r_, ins):
  rock_i = r_ % len(rocks)
  fallStep = False
  pattern = rocks[rock_i]
  b.addRock(pattern)
  # if debug:
  #  print(b)
  '''rock = b.rock
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
  ins = ins[4:] + ins[:4]'''
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
  #b.simplify()
  return ins

def getScoreCycle():
  global rocks
  ins = resetIns()
  b = Board(7)
  scores = []
  lastIdx = -1
  i=0
  for r_ in range(len(ins)*len(rocks)):
    ins = dropRock(b,r_,ins)
  lastScore = b.getHeight()
  while len(scores) < len(ins)*len(rocks):
    r_ += 1
    ins = dropRock(b,r_,ins)
    score = b.getHeight()-lastScore
    lastScore=b.getHeight()
    scores.append(score)
  cycle = findRepeat(scores)
  return cycle,scores[:cycle]

def findRepeat(seq):
  guess = 1
  max_len = len(seq) // 4
  for x in range(2, max_len):
    if seq[0:x] == seq[x:2 * x] and seq[x:2 * x] == seq[2 * x:3 * x] and seq[2 * x:3 * x] == seq[3 * x:4 * x]:
      #guess = max(guess, x)
      return x

  return guess

def resetIns():
  ins = open('input.txt').read().strip()
  ins_ = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
  return ins

if __name__ == '__main__':

  rocks = ['####',' # \n###\n # ','  #\n  #\n###','#\n#\n#\n#','##\n##']

  WIDTH=7
  fallStep = False
  p1 = False
  iter = 2022 if p1 else 1000000000000
  #floorCycleLen = 7 if len(ins) < 100 else 242

  scoreCycleLen, scoreCycle = getScoreCycle()
  print(scoreCycleLen)
  print(scoreCycle)

  ins = resetIns()

  b = Board(WIDTH)

  if iter < 10000 and False:
    scores = []
    lastScore = 0
    for r_ in range(iter):
      ins = dropRock(b,r_,ins)
      scores.append(b.getHeight()-lastScore)
      lastScore = b.getHeight()
    print(scores)
    print(sum(scores))
    quit(0)
  '''floors = []
  i=0
  while i<200000:
    ins = dropRock(b,i,ins)
    i+=1
    f = b.field
    if f in floors:
      print(floors.index(f))
    floors.append(f)'''

  #Plan: First and last loop are scuffed so they have to be calced seperately
  #Calc first loop, then calc second loop. Second loop * total loops-2, then calc last loop

  firstLen = len(ins)*len(rocks)
  firstCycle = 0
  firstCycleSize = (27,100)[1]
  scoreCycleLen = (35,1715)[1]
  debugScores = []
  #35 for testin, 27 to skip start
  #1730 for realin, 100 to skip start
  lastScore = 0
  for r_ in range(firstCycleSize):
    ins = dropRock(b, r_, ins)
    debugScores.append(b.getHeight()-lastScore)
    lastScore = b.getHeight()
  firstCycle = b.getHeight()

  scoreCycleRecalc = []
  lastScore = b.getHeight()
  for _ in range(scoreCycleLen):
    r_ += 1
    ins = dropRock(b, r_, ins)
    scoreCycleRecalc.append(b.getHeight()-lastScore)
    debugScores.append(b.getHeight()-lastScore)
    lastScore = b.getHeight()
  print(debugScores+scoreCycleRecalc)
  print(scoreCycleRecalc)
  cycles = (iter-firstCycleSize)//scoreCycleLen
  lastCycles = (iter-firstCycleSize)%scoreCycleLen
  print(firstCycle+sum(scoreCycleRecalc)*cycles+sum(scoreCycleRecalc[:lastCycles]))

