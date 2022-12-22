from pprint import pprint
from collections import deque

def calc(monkeys, m):
  if type(m) == int:
    return m
  else:
    match m[1]:
      case '+':
        m = calc(monkeys,monkeys[m[0]]) + calc(monkeys,monkeys[m[2]])
        return m
      case '-':
        m = calc(monkeys,monkeys[m[0]]) - calc(monkeys,monkeys[m[2]])
        return m
      case '*':
        m = calc(monkeys,monkeys[m[0]]) * calc(monkeys,monkeys[m[2]])
        return m
      case '/':
        m = calc(monkeys,monkeys[m[0]]) // calc(monkeys,monkeys[m[2]])
        return m

def calc2(monkeys, mName, symbolics = {'humn':'H'}):
  m = monkeys[mName]
  symbolic = False
  if mName in symbolics.keys():
    symbolic = True
    return symbolics[mName], symbolic
  if mName == 'root':
    return '(' + str(calc2(monkeys, m[0], symbolics)[0]) + ') == (' + str(calc2(monkeys, m[2], symbolics)[0]) + ')', symbolic

  if type(m) == int:
    return m, False
  else:
    match m[1]:
      case '+':
        l,ls = calc2(monkeys,m[0],symbolics)
        r,rs = calc2(monkeys,m[2],symbolics)
        if ls or rs:
          symbolics[mName] = '(' + str(l) + '+' + str(r) + ')'
          symbolic = True
          return symbolics[mName], symbolic
        return l + r, False
      case '-':
        l,ls = calc2(monkeys,m[0],symbolics)
        r,rs = calc2(monkeys,m[2],symbolics)
        if ls or rs:
          symbolics[mName] = '(' + str(l) + '-' + str(r) + ')'
          symbolic = True
          return symbolics[mName], symbolic
        return l - r, False
      case '*':
        l,ls = calc2(monkeys,m[0],symbolics)
        r,rs = calc2(monkeys,m[2],symbolics)
        if ls or rs:
          symbolics[mName] = '(' + str(l) + '*' + str(r) + ')'
          symbolic = True
          return symbolics[mName], symbolic
        return l * r, False
      case '/':
        l,ls = calc2(monkeys,m[0],symbolics)
        r,rs = calc2(monkeys,m[2],symbolics)
        if ls or rs:
          symbolics[mName] = '(' + str(l) + '/' + str(r) + ')'
          symbolic = True
          return symbolics[mName], symbolic
        return l // r, False


if __name__ == '__main__':
  ins = open('input.txt').read().strip().split('\n')
  ins_ = ''''''.split('\n')


  monkeys = {}
  for l in ins:
    m = l.split(': ')
    if ' ' in m[1]:
      m1,op,m2 = m[1].split(' ')
      m[1] = [m1,op,m2]
    else:
      m[1] = int(m[1])
    monkeys[m[0]] = m[1]

  print(len(monkeys))
  print(monkeys)
  print(calc(monkeys, monkeys['root']))
  s = calc2(monkeys, 'root')[0]
  print(s)
  print(len(s))
