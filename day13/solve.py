from pprint import pprint
from collections import deque

def comp(a,b, indent=0):
  # 1=a>b, -1=a<b 0=a==b
  print(F"{chr(9)*indent}Testing\n{chr(9)*indent}{a}\n{chr(9)*indent}{b}\n")
  if type(a) is int and type(b) is int:
    if a < b:
      return -1
    if a == b:
      return 0
    else:
      return 1

  if type(a) is int and type(b) is list:
    a = [a]

  if type(b) is int and type(a) is list:
    b = [b]

  if type(a) is list and type(b) is list:
    if len(a) == 0:
      if len(b) == 0:
        print("Two empty lists a==b")
        return 0
      print("empty a, full b; a<b")
      return -1
    for j in range(len(a)):
      if j >= len(b):
        print(F"b ran out of items first\n")
        return 1
      res = comp(a[j],b[j],indent+1)
      if res == 1:
        return 1
      if res == -1:
        return -1
    if j+1 < len(b):
      return -1
    return 0


if __name__ == '__main__':
  ins = open('input.txt').read().strip().split('\n\n')
  ins_ = '''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]'''.split('\n\n')

  ordered = []
  for i,line in enumerate(ins):
    a,b = line.split('\n')
    a.replace('[]','[-1]')
    b.replace('[]','[-1]')
    a = eval(a)
    b = eval(b)
    if comp(a,b) == -1:
      ordered.append(i+1)
      print(F"Appending {i+1}\n\t{ordered}")

  print(ordered)
  print(sum(ordered))

  from functools import cmp_to_key
  ins2 = []
  for l in ins:
    a,b = l.split('\n')
    ins2.append(eval(a))
    ins2.append(eval(b))
  ins2.append([[2]])
  ins2.append([[6]])
  ins2.sort(key=cmp_to_key(comp))
  pprint(ins2)
  print(ins2.index([[2]])+1)
  print(ins2.index([[6]])+1)
  print((ins2.index([[2]])+1)*(ins2.index([[6]])+1))
