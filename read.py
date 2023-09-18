import json

with open('guns_feature_dict.json', 'r') as f:
    loaded_dict = json.load(f)

print(loaded_dict)
