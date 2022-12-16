from pprint import pprint
from collections import deque


def getDist(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

sensors = [] #( (x,y), (bX,bY), (dX,dY), dX+dY )
maxLen = 4000000
def doWork(args):
  y = args[0]
  sensors = args[1]
  knownBases = [a[1] for a in sensors]
  for x in range(maxLen):
    cur = (x, y)
    if y%40000 == 0 and x%40000 == 0:
      print(cur)
    good = True
    for s in sensors:
      if getDist(cur, s[0]) <= s[3] or cur in knownBases:
        good = False
        break
    if good:
      print('*'*30+'\n'+cur+'\n'+'*'*30)
      return cur


if __name__ == '__main__':
  ins = open('input.txt').read().strip().split('\n')
  ins_ = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.split('\n')





  rowRange = (1e20,-1e20)

  for l in ins:
    s = l.split(' ')
    sX = int(s[2].split('=')[-1][:-1])
    sY = int(s[3].split('=')[-1][:-1])

    bX = int(s[-2].split('=')[-1][:-1])
    bY = int(s[-1].split('=')[-1])

    dist = getDist((sX,sY),(bX,bY))

    rowRange = (min(rowRange[0],sX-dist),max(rowRange[1],sX+dist))

    sensors.append(((sX,sY),(bX,bY),(bX-sX,bY-sY),dist))
    print(F"Sensor at {(sX, sY)}; nearest beacon at {(bX,bY)}")
    print(sensors[-1])


  #Y_CHECK = 2000000
  #goods = 0
  #
  #print(F"Checking from {rowRange[0]} to {rowRange[1]}")
  #for x in range(rowRange[0],rowRange[1],1):
  #  cur = (x,Y_CHECK)
  #  #print(cur)
  #  if any([getDist(cur, a[0]) <= a[3] and cur != a[1] for a in sensors]):
  #    goods += 1
  #    #print(cur)
  #  elif cur not in [a[1] for a in sensors]:
  #    print(cur)
  #    print(cur[0]*4000000+cur[1])
  #
  #print(goods)



  searchRange = (0,maxLen)

  done = False
  x = 0
  y = 0
  while not done:
    cur = (x,y)
    if y%40000 == 0 and x%40000 == 0:
      print(cur)
    done = True
    skip = 1
    for s in sensors:
      if getDist(cur,s[0]) > s[3]: #If we're farther than the sensor's beacon, ignore
        continue
      done = False                 #If we're closer than the beacon, we can skip some
      dy = abs(s[0][1]-y)
      dx = abs(s[0][0]-x) + (s[3] - dy)   #Distance to sensor + right hand possible distance to beacon
      skip = dx+1                         #1 for the sensor itself
      break
    if done:
      print(cur)
      print(cur[0]*4000000+cur[1])
      quit(0)
    x += skip
    if x>maxLen:
      y += 1
      x = x%maxLen
    if y > maxLen:
      print("Failed...")
      done = True


  #from multiprocessing import Pool
  #p = Pool()
  #args = [(a,sensors) for a in range(maxLen)]
  #res = list(p.imap_unordered(doWork,args))
  #print(len(res))
  #p.close()
  #print('done')
