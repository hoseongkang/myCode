def solution(n):
    arrList = []
    for i in range(1, n+1):
        if divmod(n,i)[1] == 0:
            arrList.append(i)
    return sum(arrList)

#input : 12 = 28 / 
#12�� ����� 1, 2, 3, 4, 6, 12. ��� ���ϸ� 28