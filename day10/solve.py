from pprint import pprint
from collections import deque

ins = open('input.txt').read().split('\n')

ins_ = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''.split('\n')

ins_ = '''noop
addx 3
addx -5'''.split('\n')


W = 40
H = 6
screen = [['.']*W for _ in range(H)]

def drawScreen(t,X):
  t = t%(40*6)
  vPos = t//40
  hPos = t%40
  sprite = ':::::'+'.'*40
  sprite = sprite[:X+4]+'###'+sprite[X+7:]
  print(X)
  print(sprite[5:])
  print()
  assert len(sprite) >= 45
  screen[vPos][hPos] = sprite[hPos+5]
  print('\n'.join([''.join(a) for a in screen]))
  print('-'*50)
  return

X = 1
pipeline = deque()
ans = 0
for i,line in enumerate(ins):
  ins = 0
  val = 0
  if len(line.split(' ')) == 2:
    ins,val = line.split(' ')
  else:
    ins = line
  if ins == 'addx':
    pipeline.append(0)
    pipeline.append(int(val))
  if ins == 'noop':
    pipeline.append(0)
  if i+1 == 20 or ((i+1) > 40 and (i-19) % 40 == 0):
    #print(i+1,(i+1)*X)
    ans += (i+1)*X
  #print(F"During {i+1}:\t{X}\t{line}\t{pipeline}")
  drawScreen(i,X)
  if len(pipeline):
    X += pipeline.popleft()
  #print(F"After {i+1}:\t{X}\t{line}\t{pipeline}")
#print('Finishing pipeline')
while len(pipeline):
  i += 1
  if i+1 == 20 or ((i+1) > 40 and (i-19) % 40 == 0):
    #print(i+1,(i+1)*X)
    ans += (i+1)*X
  drawScreen(i,X)
  X += pipeline.popleft()
  #print(F"After {i+1}:\t{X}\t{pipeline}")

print(ans)

