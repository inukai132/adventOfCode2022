import random
from pprint import pprint
from collections import deque

def bfs(graph, frm, to):
  q = deque()
  visited = []
  q.append((frm,[frm]))
  visited.append(frm)
  while(len(q)):
    cur, path = q.popleft()
    if cur == to:
      return path
    visited.append(cur)
    for next in graph[cur][2]:
      if next in visited or next in [a[0] for a in q]:
        continue
      q.append((next,path+[next]))

def score(graph, time, cur, to):
  path = bfs(graph, cur, to)
  time -= len(path)
  if time <= 0:
    return 0
  return graph[to][1] * time

def search(graph, time, cur, ons):
  #Get list of rated closed valves, sort descending
  #rate*(timeLeft-distance-1) is the score
  if time <= 0:
    return [0,[]]
  best = [0,[]]
  if time > 0:
    cands = [graph[a] for a in graph.keys() if graph[a][1] and a not in ons]
    cands.sort(key=lambda x:x[1],reverse=True)
    for c in cands:
      path = bfs(graph, cur, c[0])
      timeUsed = len(path)+1-1
      if timeUsed > time:
        continue
      ons_ = ons.copy()
      ons_.append(c[0])
      s = search(graph, time-timeUsed, c[0], ons_)
      s[0] += graph[c[0]][1] * (time-timeUsed)
      if s[0] > best[0]:
        best[0] = s[0]
        best[1] = [cur]+s[1]
        #print(F"New best {str(best)}")
  return best

import itertools

def elephantSearch(graph, time, cur0, cur1, ons, level = 0):
  #Get list of rated closed valves, sort descending
  #rate*(timeLeft-distance-1) is the score
  if time <= 0:
    return [[0,[]],[0,[]]]
  best = [[0,[]],[0,[]]]
  bestSum = sum([a[0] for a in best])

  cands = [graph[a] for a in graph.keys() if graph[a][1] and a not in ons]
  cands.sort(key=lambda x:x[1],reverse=True)

  if len(cands) == 1:
    path0 = bfs(graph, cur0, cands[0][0])
    path1 = bfs(graph, cur1, cands[0][0])
    chose0 = len(path0) < len(path1)
    cur  = cands[0]
    path = path0 if chose0 else path1
    timeUsed = len(path)
    if chose0:
      best[0][0] += graph[cur[0]][1] * (time-timeUsed)
      best[0][1] = [cur[0]]
    else:
      best[1][0] += graph[cur[0]][1] * (time-timeUsed)
      best[1][1] = [cur[0]]
    #print((time, cur0, cur1, ons, level))
    #print(cands[0])
    #print(best)
    #print()
    return best

  for cand0,cand1 in itertools.permutations(cands,2):
    path0 = bfs(graph, cur0, cand0[0])
    path1 = bfs(graph, cur1, cand1[0])
    nextTS = min(len(path0),len(path1))
    if nextTS > time:
      continue
    c0 = graph[path0[nextTS-1]]
    c1 = graph[path1[nextTS-1]]
    ons_ = ons.copy()
    if len(path0) == nextTS:
      ons_.append(c0[0])
    if len(path1) == nextTS:
      ons_.append(c1[0])
    s0,s1 = elephantSearch(graph, time-nextTS, c0[0], c1[0], ons_, level + 1)


    if sum([a[0] for a in [s0, s1]]) > bestSum:
      if len(path0) == nextTS:
        best[0][0] = s0[0]+(graph[c0[0]][1] * (time-nextTS))
        best[0][1] = [cand0[0]]+s0[1]
      if len(path1) == nextTS:
        best[1][0] = s1[0]+(graph[c1[0]][1] * (time-nextTS))
        best[1][1] = [cand1[0]]+s1[1]
      if len(path0) != nextTS:
        best[0][0] = s0[0]
        best[0][1] = s0[1]
      if len(path1) != nextTS:
        best[1][0] = s1[0]
        best[1][1] = s1[1]
      bestSum = sum([a[0] for a in best])
    #if level == 0:
    #print((time, cur0, cur1, ons, level))
    #print(cands)
    #print(cand0,cand1)
    #print(best)
    #print(bestSum)
    #print()
  return best

def bestPossible(cands, t):
  score = 0
  for i in range(0,len(cands),2):
    score += cands[i][1]*(t-2*(i))
    score += cands[i+1][1]*(t-2*(i))
  return score

def runThread(ins):
  global graph
  cur0, cur1 = ins
  ons = [cur0, cur1]
  loc0 = 'AA'
  loc1 = 'AA'
  t0 = 26
  t1 = 26
  score = 0
  path0 = bfs(graph,loc0,cur0)
  path1 = bfs(graph,loc1,cur1)
  t0 -= len(path0)
  score += graph[cur0][1]*t0
  t1 -= len(path1)
  score += graph[cur1][1]*t1

  score+=elSearch2(graph, cur0, cur1, t0, t1, ons)
  print(score)

def elSearch2(graph, cur0='AA', cur1='AA', curT0=26, curT1=26, ons=[]):
  if curT0 <= 0 and curT1 <= 0:
    return 0

  cands = [a for a in graph.keys() if graph[a][1] and a not in ons]
  cands.sort(key=lambda x:graph[x][1],reverse=True)
  cands_ = [graph[a] for a in cands]

  #if cb > bestPossible(cands_, curT0) and cb > bestPossible(cands_, curT1):
  #  return 0

  globalBest = 0

  if len(cands) == 1:
    print('a')
  for cand0, cand1 in itertools.permutations(cands, 2):
    ons_ = ons.copy()
    loc0 = cur0
    loc1 = cur1
    t0 = curT0
    t1 = curT1
    score = 0
    path0 = bfs(graph,loc0,cand0)
    path1 = bfs(graph,loc1,cand1)
    if t0 >= len(path0):
      ons_.append(cand0)
      t0 -= len(path0)
      score += graph[cand0][1]*t0
      loc0 = cand0

    if t1 >= len(path1):
      ons_.append(cand1)
      t1 -= len(path1)
      score += graph[cand1][1]*t1
      loc1 = cand1

    if t0 == curT0 and t1 == curT1:
      return 0

    score += elSearch2(graph, loc0, loc1, t0, t1, ons_)

    if score > globalBest:
      globalBest = score
  return globalBest










#  cands = cands[:10]
#  scored = []
#  best = 0
#  startLoc = (cur0,cur1)
#  for s in range(len(cands)):
#    candsPerms = list(itertools.permutations(cands))
#    print(f"{len(candsPerms)} permutations")
#    for order in candsPerms:
#      work = (order[:s],order[s:])
#      if work in scored:
#        continue
#      scored.append(work)
#      score = 0
#      for p in range(2):
#        myVisits = work[p]
#        curLoc = startLoc[p]
#        curTime = curT
#        for visit in myVisits:
#          path = bfs(graph,curLoc,visit)
#          if len(path) > curTime:
#            continue
#          curTime -= len(path)
#          curLoc = visit
#          score += graph[curLoc][1]*curTime
#      if score > best:
#        best = score
#  return best



ins = open('input.txt').read().strip().split('\n')
ins_ = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''.split('\n')


graph = {}
for line in ins:
  words = line.split(' ')
  name = words[1]
  rate = int(words[4].split('=')[-1][:-1])
  cons = [w.strip(',') for w in words[9:]]
  #print(f"{name} has rate {rate} and cons {cons}")
  graph[name] = [name, rate, cons, False]


def makeLUT(graph, start):
  LUT = {}
  cands = [start]+[a for a in graph.keys() if graph[a][1]]
  for frm in cands:
    dists = {}
    for to in cands:
      path = bfs(graph,frm,to)
      dists[to] = len(path)
    LUT[frm] = dists
  return LUT

def score(graph, paths, LUT):
  score = 0
  for i,p in enumerate(paths):
    t=26
    cur = 'AA'
    for step in p:
      dst = LUT[cur][step]
      if dst > t:
        break
      t -= dst
      score += graph[step][1]*t
      cur = step
  return score

def init_pop(graph):
  outs = [[], []]
  for k in [a for a in graph.keys() if graph[a][1]]:
    outs[random.randint(0,1)].append(k)
  return outs

def crossover(graph, p0, p1):
  crossPoint = random.randint(1,min(len(p0),len(p1))-1)

  out = p0[:crossPoint]+p1[crossPoint:]
  out = [[o for i,o in enumerate(out[0]) if o not in out[1] ],[o for i,o in enumerate(out[1]) if o not in out[0] ]]
  if len(out[0])+len(out[1]) != len([a for a in graph.keys() if graph[a][1]]):
    for k in [a for a in graph.keys() if graph[a][1]]:
      if k not in out[0] and k not in out[1]:
        out[random.randint(0,1)].append(k)

  return out


def geneMeme(graph, pops, LUT, n_iter=10000, mortRate=.5):
  popSize = len(pops)
  best = 0
  for i in range(n_iter):
    scores = [(score(graph, pop, LUT), pop) for pop in pops]
    scores.sort(key=lambda x:x[0], reverse=True)
    if best < scores[0][0]:
      print(F"{i}: max score was {scores[0]}")
      best = scores[0][0]
    pops = [p[1] for p in scores[:int(len(scores)*mortRate)]]
    while len(pops) != popSize:
      retries = 0
      new = crossover(graph,random.choice(pops),random.choice(pops))
      if new in pops and retries < 100:
        new = init_pop(graph)
      pops.append(new)






if __name__ == '__main__':
  distanceLUT = makeLUT(graph, "AA")
  pop = [init_pop(graph) for _ in range(100)]
  geneMeme(graph, pop, distanceLUT, mortRate=.9)
