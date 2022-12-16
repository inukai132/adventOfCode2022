from pprint import pprint

start, lines = open('input.txt').read().split('\n\n')
start = start.split('\n')
lines = lines.split('\n')
stacks = ['']*9
for i in range(9):
  for j in range(len(start)-1):
    if i*4+1 < len(start[j]) and start[j][i*4+1] != ' ':
      stacks[i] += start[j][i*4+1]
  stacks[i] = stacks[i][::-1]

pprint(stacks)

for line in lines:
  _,count,_,frm,_,to = line.split(' ')
  count = int(count)
  frm = int(frm)-1
  to = int(to)-1


  stacks[to] += stacks[frm][-count:]
  stacks[frm] = stacks[frm][:-count]

for s in stacks:
  print(s[-1],end='')