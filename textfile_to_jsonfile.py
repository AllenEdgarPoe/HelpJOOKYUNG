import os
import re
import json
path = r'C:\Users\chsjk\Documents\data\AI서울 참고이미지\processed'

json_data = dict()

with open(os.path.join(path, 'description.txt'), 'r', encoding='utf-8') as f:
    descriptions = f.readlines()

for description in descriptions:
    match = re.findall('(.+\.jpg) : (.+)\n', description)
    json_data[match[0][0]] = match[0][1]

with open(os.path.join(path, 'description.json'), 'w', encoding='utf-8') as f:
    json.dump(json_data, f)
