import math
from mmh3 import hash as m3h
import sys
from Element import Element


class Shifting_BloomFilter_M(object):
    """description of class"""

    def __init__(self, k, m, w):
        self.m = m - w  # the length  # m = mAF * bAF * bpeAF(包含finger和counter)
        self.k = k  # the half number of hash functions  #k = K/2
        self.vector = [0] * (m + w)  # the array
        self.w = w  # using w = 25 for 32−bit and w = 57 for 64−bit architecture

    def insert(self, content):
        for j in range(self.k):  # set the bits for membership as 1s
            hash_ = m3h(content, j + 1) % self.m
            offset = m3h(content, self.k + 1) % (self.w - 1) + 1
            try:
                self.vector[hash_] = 1  # set the bits for multiplicity
                self.vector[hash_ + offset] = 1
            except:  # may not success
                pass

    def query(self, content):  # max is the maximum multiplicity in the whole set
        for j in range(self.k):
            hash_ = m3h(content, j + 1) % self.m
            offset = m3h(content, self.k + 1) % (self.w - 1) + 1
            if self.vector[hash_] == 0 or self.vector[hash_ + offset] == 0:
                return False
        return True
