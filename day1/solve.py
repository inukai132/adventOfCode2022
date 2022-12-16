lines = open('input.txt').read().split('\n\n')
totals = []

for group in lines:
  total = sum([int(a) if len(a) else 0 for a in group.split('\n')])
  totals.append(total)

print(sum(sorted(totals,reverse=True)[:3]))