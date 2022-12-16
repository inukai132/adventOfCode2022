from pprint import pprint
from collections import deque

class monkey:
  def __init__(self, data):
    lines = data.split('\n')
    self.id = int(lines[0].split(' ')[-1].split(':')[0])
    self.items = [int(a) for a in lines[1].split(': ')[-1].split(', ')]
    self.op = (lines[2].split(': ')[-1].split(' ')[-2], lines[2].split(': ')[-1].split(' ')[-1])
    self.test = int(lines[3].split(' ')[-1])
    self.testTrue = int(lines[4].split(' ')[-1])
    self.testFalse = int(lines[5].split(' ')[-1])
    self.mb = 0

  def inspect(self, monkeys):
    while len(self.items):
      old = self.items[0]
      new = 0
      if self.op[0] == '*':
        if self.op[1] == 'old':
          new = old * old
        else:
          new = old * int(self.op[1])
      if self.op[0] == '+':
        if self.op[1] == 'old':
          new = old + old
        else:
          new = old + int(self.op[1])
      new %= 2*5*3*13*11*7*19*17
      #new %= 23*19*13*17

      #new //= 3
      self.items[0] = new
      if (self.items[0] % self.test):
        self.throwTo(monkeys[self.testFalse])
      else:
        self.throwTo(monkeys[self.testTrue])
      self.mb += 1

  def throwTo(self, target):
    target.items.append(self.items.pop(0))

  def __repr__(self):
    return f"Monkey {self.id}: {self.items}\t{self.mb}"

ins = open('input.txt').read().split('\n\n')

ins_ = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''.split('\n\n')

monkeys = [monkey(a) for a in ins]

for i in range(10000):
  for monk in monkeys:
    monk.inspect(monkeys)
  if not i%1000:
    print(i)
    for m in monkeys:
      print(m)

mb = [a.mb for a in monkeys]
print(mb)
mb.sort()

print(mb[-1]*mb[-2])
