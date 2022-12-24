from copy import deepcopy
from pprint import pprint
from collections import deque
import string

def printMap(faces, curPos = None):
  global taken, faceULCorners, headings
  pFaces = deepcopy(faces)
  map = []
  for i in range(50):
    map.append(' '*50+pFaces[1][i]+pFaces[0][i])
  for i in range(50):
    map.append(' '*50+pFaces[2][i]+' '*50)
  for i in range(50):
    map.append(pFaces[4][i]+pFaces[3][i]+' '*50)
  for i in range(50):
    map.append(pFaces[5][i]+' '*100)

  for step in taken:
    tPos = [step[0] + faceULCorners[step[2] - 1][0], step[1] + faceULCorners[step[2] - 1][1]]
    map[tPos[1]] = map[tPos[1]][:tPos[0]] + ">V<^"[headings.index(step[3])] + map[tPos[1]][tPos[0]+1:]
  if curPos:
    tPos = [curPos[0] + faceULCorners[curPos[2] - 1][0], curPos[1] + faceULCorners[curPos[2] - 1][1]]
    map[tPos[1]] = map[tPos[1]][:tPos[0]] + ">V<^"[headings.index(curHead)] + map[tPos[1]][tPos[0]+1:]
  print('\n'.join(map))
  return '\n'.join(map)



def nextToken(s):
  alpha = True
  if s[0] in string.digits:
    alpha = False
  o = ''
  i = 0
  while i < len(s) and (s[i] in string.digits) != alpha:
    o += s[i]
    i+=1

  if not alpha:
    o = int(o)
  return o, s[i:]

if __name__ == '__main__':
  ins = open('input.txt').read().split('\n\n')
  ins_ = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''.split('\n\n')

  pathS = ins[1].strip()
  path = []
  board = ins[0].split('\n')
  width = max([len(i) for i in board])
  height = len(board)
  board = [b.ljust(width) for b in board]

  while len(pathS):
    t,pathS = nextToken(pathS)
    path.append(t)

  headings = [(1,0),(0,1),(-1,0),(0,-1)]
  curHead = headings[0]
  curPos = [min([board[0].index('.'), board[0].index('#')]),0]


  for inst in path:
    match inst:
      case 'L':
        curHead = headings[(headings.index(curHead)-1)%4]
      case 'R':
        curHead = headings[(headings.index(curHead)+1)%4]
      case _:
        for _ in range(inst):
          newPos = [(curPos[i]+curHead[i])%[width,height][i] for i in range(2)]
          match board[newPos[1]][newPos[0]]:
            case '#':
              break
            case '.':
              curPos = newPos
              continue
            case ' ':
              while board[newPos[1]][newPos[0]] == ' ':
                newPos = [(newPos[i]+curHead[i])%[width,height][i] for i in range(2)]
              match board[newPos[1]][newPos[0]]:
                case '#':
                  break
                case '.':
                  curPos = newPos
                  continue

  print(curPos)
  print(curHead)
  print(1000*(curPos[1]+1)+4*(curPos[0]+1)+headings.index(curHead))

  nets = {
    1:(
      (6,'d'),
      (4,'r'),
      (3,'r'),
      (2,'r')),
    2:(
      (6,'l'),
      (1,'l'),
      (3,'u'),
      (5,'l')),
    3:(
      (2,'d'),
      (1,'d'),
      (4,'u'),
      (5,'u')),
    4:(
      (3,'d'),
      (1,'r'),
      (6,'r'),
      (5,'r')),
    5:(
      (3,'l'),
      (4,'l'),
      (6,'u'),
      (2,'l')),
    6:(
      (5,'d'),
      (4,'d'),
      (1,'u'),
      (2,'u')),
  }
  faceULCorners = (
    (100,0),
    (50,0),
    (50,50),
    (50,100),
    (0,100),
    (0,150)
  )
  #    21
  #    3
  #   54
  #   6
  faces = []
  for corner in faceULCorners:
    face = []
    for y in range(50):
      face.append(board[corner[1]+y][corner[0]:corner[0]+50])
      #face[-1] = face[-1].replace('#','.')
    faces.append(face)

  curPos = [0,0,2] #x,y,face; x and y are unfolded coords
  curHead = headings[0]
  #path = [5,'R',5,'L',200,'L','L',200,'L',200,'R','R',200,'L',50,'R',200,'R','R',200]
  taken = []
  for i,inst in enumerate(path):
    #open('debug.txt','w').write(printMap(faces, curPos))
    print(inst)
    match inst:
      case 'L':
        curHead = headings[(headings.index(curHead)-1)%4]
      case 'R':
        curHead = headings[(headings.index(curHead)+1)%4]
      case _:
        for _ in range(inst):
          newPos = [(curPos[i]+curHead[i]) for i in range(2)]
          newFace = curPos[2]
          if newPos[0] < 0: #We moved left off the face
            newFace,enterDir = nets[curPos[2]][3]
            match enterDir:
              case 'u':
                newPos = [newPos[1],0]
                curHead = headings[1]
              case 'd':
                print(f"HELP L->D {curPos} , {inst}, {newPos}")
                quit(-1)
              case 'l':
                newPos = [0,49-newPos[1]]
                curHead = headings[0]
              case 'r':
                newPos = [49,newPos[1]]
                curHead = headings[2]
          if newPos[0] >= 50: #We moved right off the face
            newFace,enterDir = nets[curPos[2]][1]
            match enterDir:
              case 'u':
                print(f"HELP R->U {curPos} , {inst}, {newPos}")
                quit(-1)
              case 'd':
                newPos = [newPos[1],49]
                curHead = headings[3]
              case 'l':
                newPos = [0,newPos[1]]
                curHead = headings[0]
              case 'r':
                newPos = [49,49-newPos[1]]
                curHead = headings[2]
          if newPos[1] < 0: #We moved up off the face
            newFace,enterDir = nets[curPos[2]][0]
            match enterDir:
              case 'u':
                print(f"HELP U->U {curPos} , {inst}, {newPos}")
                quit(-1)
              case 'd':
                newPos = [newPos[0],49]
                curHead = headings[3]
              case 'l':
                newPos = [0,newPos[0]]
                curHead = headings[0]
              case 'r':
                print(f"HELP U->R {curPos} , {inst}, {newPos}")
                quit(-1)
          if newPos[1] >= 50: #We moved down off the face
            newFace,enterDir = nets[curPos[2]][2]
            match enterDir:
              case 'u':
                newPos = [newPos[0],0]
                curHead = headings[1]
              case 'd':
                print(f"HELP D->D {curPos} , {inst}, {newPos}")
                quit(-1)
              case 'l':
                print(f"HELP D->L {curPos} , {inst}, {newPos}")
                quit(-1)
              case 'r':
                newPos = [49,newPos[0]]
                curHead = headings[2]
          match faces[newFace-1][newPos[1]][newPos[0]]:
            case '#':
              break
            case '.':
              curPos = newPos+[newFace]
              taken.append((newPos[0], newPos[1], newFace, curHead))
              continue
            case _:
              print(F"HELP I'VE LEFT THE CUBE. {newPos}, {newFace}")
              quit(-1)

  open('debug.txt', 'w').write(printMap(faces, curPos))
  tPos = [curPos[0]+faceULCorners[curPos[2]-1][0]+1,curPos[1]+faceULCorners[curPos[2]-1][1]+1]
  print(curPos)
  print(tPos)
  print(curHead)
  print(1000*(tPos[1])+4*(tPos[0])+headings.index(curHead))
