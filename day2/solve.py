ins = open('input.txt').read().split('\n')

scores_1 = {
  'A X':3,'B X':0,'C X':6,
  'A Y':6,'B Y':3,'C Y':0,
  'A Z':0,'B Z':6,'C Z':3,
}

scores_2 = {
  'A X':0+3,'B X':0+1,'C X':0+2,
  'A Y':3+1,'B Y':3+2,'C Y':3+3,
  'A Z':6+2,'B Z':6+3,'C Z':6+1,
}

def score_1(game):
  s = ord(game[2]) - ord('W') + scores_1[game]
  return s

print(sum(map(score_1, ins)))

def score_2(game):
  s = scores_2[game]
  return s

print(sum(map(score_2, ins)))
