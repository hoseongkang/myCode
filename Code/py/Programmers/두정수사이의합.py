def solution(a, b):
    return int(sorted([a,b])[1]-sorted([a,b])[0]+1)*(sum([a,b])/2)

print(solution(-11, 68))


'''
def adder(a, b):
    return sum(range(min(a,b),max(a,b)+1))

print(adder(3, 5))
'''