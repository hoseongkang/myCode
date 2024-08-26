from difflib import SequenceMatcher
import sqlite3

target = "경기도 구리시 원수택로32번길 24 (수택동, 바이오에너지상사) 101호 부오노 파스타"
postal_code = '11941'
address = '경기도 구리시 원수택로32번길 24'

query = """
SELECT * FROM restaurant
WHERE rdnPostNo LIKE ?
AND rdnWhlAddr LIKE ?;
"""

def chkMatches():
    conn = sqlite3.connect('commRes.db')
    cursor = conn.cursor()
    keywords = []
    uptaeNms = []
    try:
        cursor.execute(query, ('%' + postal_code + '%', '%' + address + '%'))

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                keywords.append(str(row[5]) + " " + str(row[6]))
                uptaeNms.append(str(row[3]))
        else:
            return [], []

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()
        return keywords, uptaeNms


def match_ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

keywords, uptaeNms = chkMatches()

if keywords:
    ratios = {keyword: match_ratio(target, keyword) for keyword in keywords}
    best_match = max(ratios, key=ratios.get)
    best_match_ratio = ratios[best_match]
    best_match_index = keywords.index(best_match)
    print(uptaeNms[int(best_match_index)])
    print("B2B")
else:
    print("B2C")
