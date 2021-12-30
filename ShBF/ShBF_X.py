import math
from mmh3 import hash as m3h
import sys
from Element import Element


class Shifting_BloomFilter_X(object):
    """description of class"""

    def __init__(self, k, m, max):
        self.m = m  # the length  # m = mAF * bAF * bpeAF(包含finger和counter)
        self.k = k  # the number of hash functions  #k = 4 and 8
        self.vector = [0] * m  # the array
        self.max = max

    def insert(self, content, multiplicity):
        for j in range(self.k):  # set the bits for membership as 1s
            hash_ = m3h(content, j + 1) % self.m
            try:
                self.vector[hash_ + multiplicity - 1] = 1  # set the bits for multiplicity
            except:  # may not success
                pass

    def query(self, content):  # max is the maximum multiplicity in the whole set
        multi = 0
        for i in range(0, self.max + 1):
            label = True
            for j in range(self.k):
                hash_ = m3h(content, j + 1) % self.m
                try:
                    if self.vector[hash_ + i] == 0:
                        label = False
                        break  # not all the k bits are non-zero
                except:  # out of range
                    pass
            if label:
                multi = i + 1
        return multi
