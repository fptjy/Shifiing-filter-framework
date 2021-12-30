import math
from mmh3 import hash as m3h
import sys
from Element import Element


class Shifting_BloomFilter_A(object):
    """description of class"""

    def __init__(self, k, m, w, sets):
        self.m = m - w  # the length  # m = mAF * bAF * bpeAF(包含finger和counter)
        self.k = k  # the half number of hash functions  #k = K/2
        self.vector = [0] * (m + w)  # the array
        self.w = w  # increment w when the number of sets is too large
        self.sets = sets  # take an example, if there is three sets 1,2,3, then sets = [1,2,3,12,13,23,123]

    def insert(self, content, mark):  # mark = [1,2], which means content belongs to set 1 and set 2.
        Mark = 0
        for i in range(len(mark)):
            Mark += mark[i] * 10 ** (len(mark) - i - 1)
        offset = 0
        for set in self.sets:
            try:
                offset += m3h(content, set) % int((self.w - 1) / len(self.sets)) + 1
                if set == Mark:
                    break
            except:
                pass

        for j in range(self.k):  # set the bits for membership as 1s
            hash_ = m3h(content, j + 1) % self.m
            try:
                self.vector[hash_ + offset] = 1  # set the bits for multiplicity
            except:  # may not success
                pass

    def query(self, content):  # max is the maximum multiplicity in the whole set
        offset = 0
        for set in self.sets:
            label = True
            offset += m3h(content, set) % int((self.w - 1) / len(self.sets)) + 1
            for j in range(self.k):
                hash_ = m3h(content, j + 1) % self.m
                try:
                    if self.vector[hash_ + offset] == 0:
                        label = False
                        break  # not all the k bits are non-zero
                except:  # out of range
                    pass
            if label:
                return set
        return False
