def solution(n):
    answer = []
    rev = 0
    n = list(map(int, str(n)))
    for i in range(len(n)):
        answer.append(n[len(n)-i-1])
    return answer

print(solution(12345))

'''def digit_reverse(n):
    return list(map(int, reversed(str(n))))
    
    =======================================================
    def digit_reverse(n):
    return [int(i) for i in str(n)][::-1]
    =======================================================
    def digit_reverse(n):
    ret =[]
    for i in str(n):
        ret.append(int(i))
    ret.reverse() 
    return ret
'''