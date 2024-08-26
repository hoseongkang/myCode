import math
import time
from datetime import datetime

def quarterYear(month):
  return math.ceil( month / 3.0 )

def currentMonth():
    if datetime.today().day > 15:
        now = time.localtime()
        return now.tm_mon - 1

print("Quarter : {}".format(quarterYear(currentMonth())))