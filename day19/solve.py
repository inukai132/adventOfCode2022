import functools
import time
from pprint import pprint
from collections import deque
import random


def step(bp, t, res, bots, plan=[]):
  if t == 0:
    return res[3],plan
  botTypes = ['ore', 'clay', 'obsidian', 'geode']
  actions = ['wait', 'ore', 'clay', 'obsidian', 'geode']
  best = [0,[]]
  for a in actions:
    plan_ = plan+[a]
    if a == 'wait':
      newRes = {b:(bots[b]+res[b]) for b in range(4)}
      s = step(bp,t-1,newRes,bots,plan_)
      if s[0] > best[0]:
        best = s
    elif a == 'ore':
      if res[0] >= bp['ore'][0]:
        newRes = {b: (bots[b] + res[b]) for b in range(4)}
        newRes[0] -= bp['ore'][0]
        newBots = {b: (bots[b]) for b in range(4)}
        newBots[0] += 1
        s = step(bp,t-1,newRes,bots,plan_)
        if s[0] > best[0]:
          best = s
    elif a == 'clay':
      if res[0] >= bp['clay'][0]:
        newRes = {b: (bots[b] + res[b]) for b in range(4)}
        newRes[0] -= bp['clay'][0]
        newBots = {b: (bots[b]) for b in range(4)}
        newBots[1] += 1
        s = step(bp,t-1,newRes,bots,plan_)
        if s[0] > best[0]:
          best = s
    elif a == 'obsidian':
      if res[0] >= bp['obsidian'][0] and res[1] >= bp['obsidian'][1]:
        newRes = {b: (bots[b] + res[b]) for b in range(4)}
        newRes[0] -= bp['obsidian'][0]
        newRes[1] -= bp['obsidian'][1]
        newBots = {b: (bots[b]) for b in range(4)}
        newBots[2] += 1
        s = step(bp,t-1,newRes,bots,plan_)
        if s[0] > best[0]:
          best = s
    elif a == 'geode':
      if res[0] >= bp['geode'][0] and res[2] >= bp['geode'][1]:
        newRes = {b: (bots[b] + res[b]) for b in range(4)}
        newRes[1] -= bp['geode'][0]
        newRes[2] -= bp['geode'][1]
        newBots = {b: (bots[b]) for b in range(4)}
        newBots[3] += 1
        s = step(bp,t-1,newRes,bots,plan_)
        if s[0] > best[0]:
          best = s

  return best


def score(ins):
  bp,plan = ins
  res = 0
  bots = 1
  for i,a in enumerate(plan):
    if a == 'wait':
      res = res+bots
    elif a == 'ore':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**0
      else:
        return i,plan
    elif a == 'clay':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**1
      else:
        return i,plan
    elif a == 'obsidian':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**2
      else:
        return i,plan
    elif a == 'geode':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**3
      else:
        return i,plan
  return (res//ENC_SCALE**3*100+i,plan)

def init_pop():
  prologueLen = TIME
  actions = ['wait', 'ore', 'clay', 'obsidian', 'geode']
  outs = tuple(random.choice(actions) for _ in range(prologueLen))
  return outs

def crossover(p0, p1, mr=.10):
  actions = ['wait', 'ore', 'clay', 'obsidian', 'geode']
  minPt = 1
  while True:
    if minPt+1 >= len(p0):
      return p0
    crossPoint = random.randint(minPt,min(len(p0),len(p1))-1)
    break

  out = p0[:crossPoint]+p1[crossPoint:] if random.randint(0,1) else p1[:crossPoint]+p0[crossPoint:]
  out = tuple(o if random.random() > mr else random.choice(actions) for o in out)

  return out


def geneMeme(bp, pops, n_iter=1000, mortRate=.5, mutRate=.05):
  from multiprocessing import Pool
  p = Pool(16)
  popSize = len(pops)
  best = -1
  used = set(pops)
  i=0
  while i < n_iter:
    if i % (n_iter//10) == 0:
      print(i,'/',n_iter)
    scores = [(s,p) for s,p in p.imap_unordered(score,[(bp,pop) for pop in pops],2)]
    #scores = [(s,p) for s,p in [score((bp,pop)) for pop in pops]]
    scores.sort(key=lambda x:x[0], reverse=True)

    if best < scores[0][0]:
      print(F"{i}: max score was {scores[0]}")
      best = scores[0][0]
      n_iter *= 1+(i/n_iter)*.25
      n_iter = int(n_iter)
    pops = set(p[1] for p in scores[:int(len(scores)*mortRate)])
    popsl = list(pops)
    maxRetry = 100
    while len(pops) <= popSize:
      new = crossover(random.choice(popsl),random.choice(popsl),mutRate)
      pops.add(new)
    i+=1
  print("Starting close search 1")
  i=11
  print(i)
  for j,pop in enumerate(scores):
    if pop[0] < 100:
      continue
    b,r = skipAhead(bp,pop[1][:-i])
    res = try3(bp,r,b, TIME-i, pop[1][:-i])
    geodes = res[0]//ENC_SCALE**3
    scores[j] = (geodes*100,res[1])
    if geodes > best//100:
      best = geodes*100
      print(F"New best is {best}")
  pops = set(p[1] for p in scores)
  i=0
  while i < n_iter:
    if i % (n_iter // 10) == 0:
      print(i, '/', n_iter)
    scores = [(s, p) for s, p in p.imap_unordered(score, [(bp, pop) for pop in pops], 2)]
    # scores = [(s,p) for s,p in [score((bp,pop)) for pop in pops]]
    scores.sort(key=lambda x: x[0], reverse=True)

    if best < scores[0][0]:
      print(F"{i}: max score was {scores[0]}")
      best = scores[0][0]
      n_iter *= 1 + (i / n_iter) * .25
      n_iter = int(n_iter)
    pops = set(p[1] for p in scores[:int(len(scores) * mortRate)])
    popsl = list(pops)
    maxRetry = 100
    while len(pops) <= popSize:
      new = crossover(random.choice(popsl), random.choice(popsl), mutRate)
      pops.add(new)
    i += 1
  print("Starting close search 2")
  i = 11
  print(i)
  for j, pop in enumerate(scores):
    if pop[0] < 100:
      continue
    b, r = skipAhead(bp, pop[1][:-i])
    res = try3(bp, r, b, TIME - i, pop[1][:-i])
    geodes = res[0] // ENC_SCALE ** 3
    if geodes > best // 100:
      best = geodes * 100
      print(F"New best is {best}")
  return best//100

def skipAhead(bp, plan):

  res = 0
  bots = 1
  for i,a in enumerate(plan):
    if a == 'wait':
      res = res+bots
    elif a == 'ore':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**0
      else:
        return i,plan
    elif a == 'clay':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**1
      else:
        return i,plan
    elif a == 'obsidian':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**2
      else:
        return i,plan
    elif a == 'geode':
      if encResTest(res, bp[a]):
        res -= bp[a]
        res += bots
        bots += 1*ENC_SCALE**3
      else:
        return i,plan
  return (bots, res)


def step2(ins):
  bp, plan_b10,res,bots,partLen = ins
  for i in range(partLen):
    step = plan_b10%5
    plan_b10 = plan_b10//5
    match step:
      case 0:
        res += bots
      case 1:
        if res%100 < bp['ore']%100:
          return (-1,0)
        res -= bp['ore']
        res += bots
        bots += 1
      case 2:
        if res%100 < bp['clay']%100:
          return (-1,0)
        res -= bp['clay']
        res += bots
        bots += 100
      case 3:
        if res%100 < bp['obsidian']%100 or (res//100)%100 < (bp['obsidian']//100)%100:
          return (-1,0)
        res -= bp['obsidian']
        res += bots
        bots += 10000
      case 4:
        if res%100 < bp['geode']%100 or (res//10000)%100 < (bp['geode']//10000)%100:
          return (-1,0)
        res -= bp['geode']
        res += bots
        bots += 1000000
  return (res,bots)

def encResTest(res,cost):
  for i in range(4):
    if res%ENC_SCALE < cost%ENC_SCALE:
      return False
    res //= ENC_SCALE
    cost //= ENC_SCALE
    if not res and not cost:
      return True
  return True


def try3(bp, res=0, bots=1, t=0, steps=[], toBeat=0):
  assert(res>=0 and bots>=0 and t>=0)
  actions = ['geode','obsidian','clay','ore']
  best = [-1,[]]
  if t >= TIME:
    return [res,steps]

  tl = TIME-t
  if res + tl*bots + tl*tl//2*ENC_SCALE**3 < toBeat:
    return best

  for a in actions:
    if not encResTest(res + bots * (TIME-t), bp[a]):
      continue
    for tx in range(t,TIME):
      if encResTest(res+bots*(tx-t),bp[a]):
        break
    tx+=1
    steps_ = tuple(list(steps) + [a])
    score = try3(bp, res+bots*(tx-t)-bp[a], bots+ENC_SCALE**(3-actions.index(a)), tx, steps_, best[0])
    if score[0] > best[0]:
      best = score
  if len(steps)==0:
    print(f"DEBUG: {best}")
  return best

ENC_SCALE=1000
TIME=32
TIME_=24

if __name__ == '__main__':
  ins = open('input.txt').read().split('\n')
  ins_ = '''Blueprint 1:  Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:  Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''.split('\n')

  bps = []
  for l in ins:
    costs = l.split(':  ')[-1].split('. ')
    botTypes = ['ore','clay','obsidian','geode']
    bp = {}
    for i,k in enumerate(botTypes):
      cost = sum([int(a.split(' ')[0])*ENC_SCALE**botTypes.index(a.split(' ')[1].strip('.')) for a in costs[i].split('costs ')[-1].split(' and ')])
      bp[k] = cost
    bps.append(bp)
  pprint(bps)

  pops = set()
  while len(pops) != 500:
    pops.add(init_pop())
  totalScores = []
  for bp in bps[2:3]:
    subScores = [geneMeme(bp,pops,1000,.5,.25) for _ in range(10)]
    print(subScores)
    print(max(subScores))
    totalScores.append(max(subScores))
    print(totalScores)


  quit(0)
  from multiprocessing import Pool
  p = Pool()
  scores = p.map(try3,bps[:3])
  print(scores)
  print(scores[0]*scores[1]*scores[2])

  quit(0)
  for i,bp in enumerate(bps):
    firstParts = {}
    partLen = 1
    res = p.map(step2, [(bp, p, 0, 1, partLen) for p in range(5 ** partLen)])
    print("Filtering results")
    for plan, resOut in enumerate(res):
      if resOut[0] >= 0:
        firstParts[plan] = resOut
    print(len(firstParts))
    lastParts = firstParts
    for j in range(partLen,24,partLen):
      print(f"Calcing {j} part")
      tmp = {}
      for plan,result in lastParts.items():
        res,bots = result
        stepRes = p.map(step2, [(bp,p,res,bots,partLen) for p in range(5 ** partLen)])
        for planNext, resOut in enumerate(stepRes):
          if resOut[0] >= 0:
            tmp[plan+planNext*5**j] = resOut
      print(len(tmp))
      lastParts = tmp.copy()

  quit(0)