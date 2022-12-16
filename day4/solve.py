ins_1 = open('input.txt').readlines()

total = 0
for line in ins_1:
  a,b = line.split(',')
  al = list(range(int(a.split('-')[0]),int(a.split('-')[1])+1))
  bl = list(range(int(b.split('-')[0]),int(b.split('-')[1])+1))
  if any([x in al for x in bl]) or any([x in bl for x in al]):
    total += 1
print(total)