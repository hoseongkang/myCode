def solution(x, n):
    answer = []
    i = 0
    while i < n:
        i+=1
        answer.append(x*i)
    return answer

#solution(2,5)


def solution_1(x, n):
    return [i * x + x for i in range(n)] 
print(solution_1(2,5))