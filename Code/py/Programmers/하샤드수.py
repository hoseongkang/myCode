def solution(x):
    return divmod(x,sum(list(map(int,str(x)))))[1] == 0
print(solution(10))
'''def solution(x):
    p = 0
    n = list(map(int,str(x)))
    for i in range(len(n)):
        p+=n[i]
    print(p)
solution(120)
'''
'''
answer = 0
n = list(map(int, str(n)))
for i in range(len(n)):
    answer+=n[i]
return answer'''