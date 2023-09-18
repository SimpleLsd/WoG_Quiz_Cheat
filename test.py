import Levenshtein

given_string = "Browning M2"

# 六个候选字符串
candidate_strings = ["BAR", "Browning M2", "DShK",
                     "Hotchkiss M1909", "Ultimax 100", "RPD"]

# 初始化最小距离和最接近的字符串索引
min_distance = float('inf')
closest_index = None

# 遍历候选字符串并计算Levenshtein距离
for index, candidate in enumerate(candidate_strings):
    distance = Levenshtein.distance(given_string, candidate)
    if distance < min_distance:
        min_distance = distance
        closest_index = index

print(closest_index)
