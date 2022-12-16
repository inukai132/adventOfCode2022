from pprint import pprint

ins = open('input.txt').read().split('\n')

TOTAL = 70000000
TARGET = 30000000

dirSizes = {}
curPath = ''
for line in ins:
  if line[0] == '$':
    if line.split(' ')[1] == 'cd':
      if line.split(' ')[-1] == '/':
        curPath = ''
      elif line.split(' ')[-1] == '..':
        curPath = '/'.join(curPath.split('/')[:-1])
      else:
        curPath += '/'+line.split(' ')[-1]
  elif line.split(' ')[0] != 'dir':
    subPath = ''
    for pathPart in curPath.split('/'):
      subPath += '/'+pathPart
      if subPath in dirSizes.keys():
        dirSizes[subPath] += int(line.split(' ')[0])
      else:
        dirSizes[subPath] = int(line.split(' ')[0])

pprint(dirSizes)
print(sum([a if a < 100000 else 0 for a in dirSizes.values()]))

print(F"There are {TOTAL-dirSizes['/']} bytes free, need to free {TARGET-(TOTAL-dirSizes['/'])}")

candidates = {}
for k,v in dirSizes.items():
  if v > TARGET-(TOTAL-dirSizes['/']):
    candidates[k]=v

pprint(candidates)
