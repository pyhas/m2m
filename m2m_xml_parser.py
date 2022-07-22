from itertools import count
import json
from rich import print

f = open('elements_test.json', 'r')
elements = json.load(f)
count = 0
for element in elements:
    count += 1
    # for apn in element['apns']:
    #     count += 1
    # print(f'{element["hostname"]} has {count} apn ')
print(count)