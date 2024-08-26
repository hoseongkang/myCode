'''
def solution(words):
    icnt = 0
    for str in words:
        for i in range(1,len(str) + 1):
            icnt = icnt + 1
            if len(list(filter(lambda x:x.startswith(str[:i]), words))) == 1: 
                break
    return icnt
'''

#["word","war","warrior","world"]
#["abc","def","ghi","jklm"]
#["go","gone","guild"]

def solution(words):
    Trie = {}                                
    for word in words:
        cur_Trie = Trie
        for w in word:
            cur_Trie.setdefault(w,[0,{}])
            cur_Trie[w][0] +=1               
            cur_Trie = cur_Trie[w][1]
            
    result = 0
    for word in words:
        cur_Trie = Trie
        for i in range(len(word)):
            if cur_Trie[word[i]][0] == 1 :   
                break
            cur_Trie = cur_Trie[word[i]][1]
        result += i+1
    return result

words = ["word","war"]
print(solution(words))