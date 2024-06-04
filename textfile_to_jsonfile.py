import os
import re
import json
parent_path = r'C:\Users\chsjk\Documents\data\해양박물관\processed'

for pp in os.listdir(parent_path):
    path = os.path.join(parent_path, pp)
    json_data = dict()

    try:
        with open(os.path.join(path, 'description.txt'), 'r', encoding='utf-8') as f:
            descriptions = f.readlines()

        for description in descriptions:
            match = re.findall('(.+\.jpg) : (.+)\n', description)
            json_data[match[0][0]] = match[0][1]

        with open(os.path.join(path, 'description.json'), 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
    except Exception as e:
        print(e)
        continue
