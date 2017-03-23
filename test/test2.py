# coding=utf-8
# tup = ("I", "AM", "CHINESE")
# print(tup[0])
# print(tup[1])
# print(tup[2])
# print(tup[-1])
# print(tup[-2])
# print(tup[-3])
#
# tup[0] = "HE"

l = ["I", "AM", "CHINESE"]  # 下标0,1,2
# for item in l:  # For循环，遍历list里面的元素
#     print item

# for index in range(-1, -1-len(l), -1):
#    print(l[index])

# index = -1  # 末尾元素
#
# while index > (-1 - len(l)):
#     print(l[index])
#     index -= 1

for index in range(0, len(l), 1):
    print(index, l[index])
