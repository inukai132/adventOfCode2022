from pprint import pprint

ins = open('input.txt').read().split('\n')

print(F"{len(ins)} x {len(ins[0])}")

trees = set()

def countLine(line, rev=False, row=-1, col=-1):
  global trees
  outs = []
  if rev:
    line = line[::-1]
    tallest = -1
    for i,t in enumerate(line):
      if int(t) > tallest:
        outs.append((row,len(line)-i-1) if row != -1 else (len(line)-i-1,col))
        tallest = int(t)
  else:
    tallest = -1
    for i,t in enumerate(line):
      if int(t) > tallest:
        outs.append((row,i) if row != -1 else (i,col))
        tallest = int(t)

  [trees.add(a) for a in outs]
  return outs


for i,row in enumerate(ins):
  countLine(row,row=i)
  countLine(row,rev=True,row=i)

for i in range(len(ins)):
  col = ''.join([a[i] for a in ins])
  countLine(col,col=i)
  countLine(col,rev=True,col=i)


#pprint(trees)
print(len(trees))

def calcScenic(x,y):
  score = 1
  self = int(ins[y][x])
  dirScore = 0

  for _y in range(y-1,-1,-1):
    dirScore += 1
    if int(ins[_y][x]) >= self:
      break

  score *= dirScore
  dirScore = 0

  for _y in range(y+1,len(ins)):
    dirScore += 1
    if int(ins[_y][x]) >= self:
      break

  score *= dirScore
  dirScore = 0

  for _x in range(x-1,-1,-1):
    dirScore += 1
    if int(ins[y][_x]) >= self:
      break

  score *= dirScore
  dirScore = 0

  for _x in range(x+1,len(ins)):
    dirScore += 1
    if int(ins[y][_x]) >= self:
      break

  score *= dirScore
  dirScore = 0


  return score

print(max([calcScenic(a,b) for a in range(len(ins)) for b in range(len(ins))]))

quit(0)