import string

space = string.ascii_lowercase+string.ascii_uppercase

ins_1 = [(a[:len(a)//2], a[len(a)//2:]) for a in open('input.txt').read().split('\n')]
ins_2 = open('input.txt').read().split('\n')

def getCom(a):
  for c in a[0]:
    if c in a[1]:
      return c

def getCom2(a):
  for c in a[0]:
    if c in a[1]:
      if c in a[2]:
        return c

coms = list(map(getCom, ins_1))
sum = 0
for p in coms:
  sum += space.find(p) + 1

print(sum)

sum = 0
for i in range(0,len(ins_2),3):
  a = ins_2[i+0]
  b = ins_2[i+1]
  c = ins_2[i+2]
  p = getCom2((a,b,c))
  sum += space.find(p) + 1
print(sum)