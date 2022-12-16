from pprint import pprint

signal = open('input.txt').read()

for i in range(len(signal)-14):
  test = signal[i:i+14]
  if len(set(test)) == 14:
    print(i)
    break