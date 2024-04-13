import re
import json

# 使用正则表达式精确查找"bbox": {xxxx}结构
pattern = r'"bbox":\s*\{(.*?)\}'


def get_bbox(s):
    match = re.search(pattern, s, re.DOTALL)  # 使用re.DOTALL使.匹配包括换行符在内的任何字符
    data = ""
    if match:
        json_string = match.group(1)
        # 如果需要将找到的JSON字符串转换为Python的dict对象
        data = json.loads('{' + json_string + '}')
        print("Loaded as dictionary:", data)
    else:
        print("No JSON found.")
    return data

#
# json_string = '{"banya": [100, 206, 40, 100], "dogwood": [0, 156, 90, 180]}'
# data = json.loads(json_string)