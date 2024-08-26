'''def solution(n):
    iCnt = 1
    while n%iCnt != 1:
        iCnt += 1
    return iCnt
    
print(solution(12))

'''

def solution(n):
    return [x for x in range(1,n+1) if n%x==1][0]
    
print(solution(12))
