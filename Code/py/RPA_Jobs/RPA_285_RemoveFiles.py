import re
 
def fText(inText):
    pattern = "[0-9]+(KG|kg)"
    match = re.search(pattern,inText)
    result  = match.group(0)
    return result

print(fText("프락토올리고당/25KG/CAN"))