def solution(babbling):
    cnt = 0
    poss = ["aya", "ye", "woo", "ma"]
    
    # ("aywom")
    for bab in babbling:
        pre = ''
        done = True
        flag = 0
        bab_val = bab
        if len(bab) < 2:
            continue
        while done:
            for p in poss:
                if bab_val[0:len(p)] in poss:
                    if bab_val[0:len(p)] == p:
                        if p*2 in bab_val:
                            done = False
                        else:
                            bab_val = bab_val[len(p):]
                        flag = 0
                elif len(bab_val) == 0:
                    done = False
                elif bab_val[0:len(p)] not in poss:
                    flag += 1
                    if flag == 4:
                        done = False

        if len(bab_val) == 0:
            cnt += 1
    return cnt

print(solution(["ayaye", "uuu", "yeye", "yemawoo", "ayaayaa"]))