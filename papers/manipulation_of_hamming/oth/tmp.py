import random
ans = 0
for i in range(10000):
  vs = [random.randint(0, 7) for _ in range(25)]
  if set(vs) == {0, 1, 2, 3, 4, 5, 6, 7}:
    ans += 1

print(ans / 10000)