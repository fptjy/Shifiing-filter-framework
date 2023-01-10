import math
from mmh3 import hash as m3h
import sys


class ElasticSketch(object):
    """description of class"""

    def __init__(self, k, m1, m2, Lambda=8):
        self.m1 = m1  # the length of heavy part array
        self.m2 = m2  # the length of light part array
        self.k = k  # the number of hash functions of light part
        self.Lambda = Lambda
        self.heavy_part = [[0, 0, 0, 0] for _ in range(m1)]
        self.light_part = [[0] * m2 for _ in range(k)]

    def insert(self, content):
        # 首先映射到heavy_part
        hashes_heavy = m3h(content, 1) % self.m1
        if self.heavy_part[hashes_heavy] == [0, 0, 0, 0]:
            self.heavy_part[hashes_heavy] = [content, 1, 0, 0]
            return True
        if self.heavy_part[hashes_heavy][0] == content:
            self.heavy_part[hashes_heavy][1] += 1
            return True
        if self.heavy_part[hashes_heavy][0] != content:
            self.heavy_part[hashes_heavy][3] += 1
            if self.heavy_part[hashes_heavy][3] / self.heavy_part[hashes_heavy][1] < self.Lambda:
                self.insert_to_CM_Sketch(content, 1)
            else:
                self.insert_to_CM_Sketch(self.heavy_part[hashes_heavy][0], self.heavy_part[hashes_heavy][1])
                self.heavy_part[hashes_heavy] = [content, 1, 1, 1]
            return True
        return False

    def insert_to_CM_Sketch(self, key, number):
        for j in range(self.k):
            hashes_light = m3h(key, j + 2) % self.m2
            self.light_part[j][hashes_light] += number
        return True

    def query(self, content):
        # 首先映射到heavy_part
        hashes_heavy = m3h(content, 1) % self.m1
        if self.heavy_part[hashes_heavy][0] != content:
            return self.query_to_CM_Sketch(content)
        else:
            if self.heavy_part[hashes_heavy][2] == 0:
                return self.heavy_part[hashes_heavy][1]
            else:
                return self.heavy_part[hashes_heavy][1] + self.query_to_CM_Sketch(content)

    def query_to_CM_Sketch(self, key):
        result = []
        for j in range(self.k):
            hashes_light = m3h(key, j + 2) % self.m2
            result.append(self.light_part[j][hashes_light])
        return min(result)
