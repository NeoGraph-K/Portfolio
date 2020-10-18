import random

Cnt = int(input('로토 번호 횟수 : '))
Result = []
for _ in range(Cnt):
    NumberList = list(range(1,46))
    for __ in range(6):
        Result.append(random.choice(NumberList))
        NumberList.remove(Result[-1])
    print(Result)
    Result = []
