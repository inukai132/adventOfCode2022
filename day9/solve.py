from pprint import pprint

ins = open('input.txt').read().split('\n')

ROPELEN=10
rope = [(0,0)]*ROPELEN

tVisits = set()
tVisits.add(rope[-1])

dr_LUT = {
  'U': (0,1),
  'D': (0,-1),
  'L': (-1,0),
  'R': (1,0)
}

lastBoard = 3
def printTable(rope):
  global lastBoard
  boardLn = max(max([abs(a[0]) for a in rope]+[abs(a[1]) for a in rope])*2+1, lastBoard)
  lastBoard = boardLn
  quadLn = (boardLn-1)//2
  board = ['.'*boardLn]*boardLn
  for knot in tVisits:
    board[knot[1]+quadLn] = board[knot[1]+quadLn][:knot[0]+quadLn]+'#'+board[knot[1]+quadLn][knot[0]+quadLn+1:]
  for i,knot in enumerate(rope):
    board[knot[1]+quadLn] = board[knot[1]+quadLn][:knot[0]+quadLn]+str(i)+board[knot[1]+quadLn][knot[0]+quadLn+1:]
  print('\n'.join(board[::-1]))
  print('\n')


for line in ins:
  dr, ln = line.split(' ')
  print(line)
  dr = dr_LUT[dr]
  ln = int(ln)
  for _ in range(ln):
    old_hPos = rope[0]
    rope[0] = (rope[0][0]+dr[0],rope[0][1]+dr[1])
    for i in range(1,len(rope)):
      if (rope[i][0]-rope[i-1][0])**2+(rope[i][1]-rope[i-1][1])**2 == 4:
        test = {
          (rope[i][0]+1-rope[i-1][0])**2+(rope[i][1]-rope[i-1][1])**2:(1,0)  ,
          (rope[i][0]-1-rope[i-1][0])**2+(rope[i][1]-rope[i-1][1])**2:(-1,0) ,
          (rope[i][0]-rope[i-1][0])**2+(rope[i][1]+1-rope[i-1][1])**2:(0,1) ,
          (rope[i][0]-rope[i-1][0])**2+(rope[i][1]-1-rope[i-1][1])**2:(0,-1),
        }
        goodDr = test[min(test.keys())]
        rope[i] = (rope[i][0]+goodDr[0],rope[i][1]+goodDr[1])
      elif (rope[i][0]-rope[i-1][0])**2+(rope[i][1]-rope[i-1][1])**2 > 2:
        test = {
          (rope[i][0]+1-rope[i-1][0])**2+(rope[i][1]+1-rope[i-1][1])**2:(1,1)  ,
          (rope[i][0]+1-rope[i-1][0])**2+(rope[i][1]-1-rope[i-1][1])**2:(1,-1) ,
          (rope[i][0]-1-rope[i-1][0])**2+(rope[i][1]+1-rope[i-1][1])**2:(-1,1) ,
          (rope[i][0]-1-rope[i-1][0])**2+(rope[i][1]-1-rope[i-1][1])**2:(-1,-1),
        }
        goodDr = test[min(test.keys())]
        rope[i] = (rope[i][0]+goodDr[0],rope[i][1]+goodDr[1])
    tVisits.add(rope[-1])
    #printTable(rope)

print(len(tVisits))