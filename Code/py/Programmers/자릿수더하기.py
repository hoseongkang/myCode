def solution(n):
    answer = 0
    n = list(map(int, str(n)))
    for i in range(len(n)):
        answer+=n[i]
    return answer

print(solution(123))
#input : 123 = 6 / 987 =24