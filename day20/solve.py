from pprint import pprint
from collections import deque

class DLLNode:
  def __init__(self,val):
    self.val = val
    self.left = None
    self.right = None

  def linkLeft(self,node):
    self.left = node
    node.right = self

  def linkRight(self,node):
    self.right = node
    node.left = self

  def __repr__(self):
    return f"Node with val {self.val}. Left: {self.left.val}. Right: {self.right.val}"



class DLL:
  def __init__(self, l = []):
    self.nodes = []
    for val in l:
      n = DLLNode(val)
      if len(self.nodes):
        n.linkLeft(self.nodes[-1])
      self.nodes.append(n)
    if len(self.nodes):
      self.nodes[-1].linkRight(self.nodes[0])

  def search(self, val):
    for n in self.nodes:
      if n.val == val:
        return n
    return None

  def shiftLeft(self,val,amt):
    assert(amt >= 0)
    n = self.search(val)
    if not n:
      return None
    amt %= len(self.nodes)-1
    if not n:
      return None
    amt %= len(self.nodes)-1
    for _ in range(amt):
      l = n.left
      ll = n.left.left
      r = n.right
      r.linkLeft(l)
      l.linkLeft(n)
      n.linkLeft(ll)

  def shiftRight(self,val,amt):
    assert(amt >= 0)
    n = self.search(val)
    if not n:
      return None
    amt %= len(self.nodes)-1
    for _ in range(amt):
      l = n.left
      r = n.right
      rr = n.right.right
      l.linkRight(r)
      r.linkRight(n)
      n.linkRight(rr)

  def get(self,startVal,idx):
    right = True
    if idx < 0:
      right = False
      idx *= -1
    cur = self.search(startVal)
    for _ in range(idx):
      if right:
        cur = cur.right
      else:
        cur = cur.left
    return cur

  def __repr__(self):
    s = ""
    c = self.nodes[0]
    for _ in range(min(50,len(self.nodes))):
      s+=str(c.val)+", "
      c = c.right

    return F"List with len {len(self.nodes)}: {s}"


def seek(dq : deque, v):
    dq.rotate(-dq.index(v))
    assert (dq[0] == v)


if __name__ == '__main__':
  ins = [int(a)*811589153 for a in open('input.txt').read().split('\n')]
  ins_ = [int(a)*811589153 for a in '''1
2
-3
3
-2
0
4'''.split('\n')]

  ring = deque()
  z = None
  for i,l in enumerate(ins):
    ring.append((l,i))
    if l == 0:
      z = (l,i)
  for _ in range(10):
    for i,l in enumerate(ins):
      seek(ring,(l,i))
      x = ring.popleft()
      ring.rotate(-l)
      ring.appendleft(x)

  s = []
  seek(ring,z)
  for x in range(3):
    ring.rotate(-1000)
    s.append(ring[0][0])

  print(s)
  print(sum(s))



'''
  ll = DLL(ins.copy())

  for l in ins:
    if l > 0:
      ll.shiftRight(l,l)
    else:
      ll.shiftLeft(l,-l)
  print(sum(ll.get(0,x).val for x in [1000,2000,3000]))
'''
