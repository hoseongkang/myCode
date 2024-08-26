from difflib import SequenceMatcher

# Define target string and keywords
target = "서울특별시 중구 명동길 73 (명동1가, YWCA연합회) 2층 몰또 사무실"
keywords = ["몰또 이탈리안 에스프레소바(Molto Italian espresso bar)", "인천광역시 옹진군 연평면 연평로167번길 12/ 2층 제이(J)호프", "인천광역시 옹진군 연평면 연평로167번길 12 포차167", "인천광역시 옹진군 연평면 연평로167번길 12 제이", "인천광역시 옹진군 연평면 연평로167번길 12/ 2층 본스치킨"]

# Function to calculate match ratio
def match_ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

# Calculate match ratios for all keywords
ratios = {keyword: match_ratio(target, keyword) for keyword in keywords}

# Find the keyword with the highest match ratio
best_match = max(ratios, key=ratios.get)
best_match_ratio = ratios[best_match]

if best_match_ratio < 0.5:
    print("B2C")
else:
    print("B2B")

print(best_match)
print(best_match_ratio)
