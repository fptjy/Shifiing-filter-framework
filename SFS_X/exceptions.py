"""
Exceptions module
"""


class CuckooFilterFullException(Exception):
    """
    Exception raised when filter is full.
    """
    pass


# import math
#
# e = 2.718281828459
#
#
# def fpr_BF(n, m, k, e):
#     x = -k * n / m
#     y = (1 - e ** x) ** k
#     return y
#
#
# k = [i for i in range(4, 20)]
# print(k)
#
# result = []
# N = 0.95 * 2 ** 20
# M = 21 * 0.95 * 2 ** 20
# E = 2.718281828459
# for i in range(len(k)):
#     result.append(fpr_BF(n=N, m=M, k=k[i], e=E))
# print(result)
#
# z = 0.0001014301518458245
#
# x1 = (1 - z) ** (2 ** 5 * 32)
# print(x1)

# SFS的准确度计算
def compute_precision_SFS(b=2, l=2, i=1):
    x = 1 - 1 / (2 ** l)
    y = x ** (4 * i)
    return y / b


b = 2 ** 5
result = 0
for i in range(b):
    result += compute_precision_SFS(b, 16, i + 1)
print(result)
print((1 - result) / 2 ** 5)


# SFB的准确度计算
def compute_precision_SFB(B=1, b=2, l=2, i=1):
    x = 1 - 1 / (2 ** l)
    y = x ** (2 * b * i)
    return y / B


B = 2 ** 5
result = 0
for i in range(B):
    result += compute_precision_SFB(B, 4, 16, i + 1)
print(result)
print((1 - result) / 2 ** 5)
