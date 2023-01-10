# z = [[0] * 3 for _ in range(2)]
# print(z)
# print(type(z))
# print(type(z[0]))
# print(z[0])
#
# x = [0, 0, 0, 0]
#
# print(x != [0, 0, 0, 0])
#
# if 3.2 < 4:
#     print("yy")
#
# import sys
#
# str1 = "17 94.22.49.56 206.211.191.163 19305 58795"
# str2 = "人生苦短，我用Python"
# x = len(str1.encode())
# print("x", x)
#
# cc = [2, 12, 5, 0]
# print("min", min(cc))
#
# data_processed = []
# with open("F:/Network_flow_data/data/4/dataset_for_experiment/files_extract_frequency.txt", "r",
#           encoding='utf-8') as file:
#     for line in file:
#         line = line.strip('\n')  # 删除换行符
#         data = line.split(":")
#         data_processed.append([data[0], int(data[1])])  # 提取频数信息
#     file.close()
#
# print(data_processed)


# data_raw = []
# with open("F:/Network_flow_data/data/4/dataset_for_experiment/files_extract_5_tuple.txt", "r",
#           encoding='utf-8') as file:
#     for line in file:
#         line = line.strip('\n')  # 删除换行符
#         data_raw.append(line)  # 提取频数信息
#     file.close()
# print(len(data_raw))
# print(data_raw[0])
# print(data_raw[1])
# print(data_raw[2])
# print(type(data_raw[0]))

Z = [0,1,2,3]
import numpy as np
s = np.mean(Z)
print(s)