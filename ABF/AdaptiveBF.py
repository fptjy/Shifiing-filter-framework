import math
from mmh3 import hash as m3h
import sys
from Element import Element

class Adaptive_BloomFilter(object):
    """description of class"""
    def __init__(self, k, m, max):
        self.m = m  # the length 
        self.k = k  # the number of hash functions  # k = 4 and 8
        self.vector = [0]*m   # the array
        self.max = max # the max multiplicity in the set 

    def insert(self,content,multiplicity):
        if self.max < multiplicity:
            print("out of max") 
            return False
        else:
            for j in range(self.k+1):  # set the bits as 1s for membership
                hash_ = m3h(content,j+1)%self.m
                self.vector[hash_] = 1 
            for i in range(1,multiplicity+1): # set the bits as 1s for multiplicity
                hash_ = m3h(content,self.k+1+i)%self.m
                self.vector[hash_] = 1 

    def query(self,content):# max is the maximum multiplicity in the whole set
        for j in range(self.k+1):
            hash_ = m3h(content,j+1)%self.m
            if self.vector[hash_] == 0:
                return False   # not a member of the set
        multi = 1 
        for i in range(1,self.max+1): 
            hash_ = m3h(content,self.k+1+i)%self.m
            if self.vector[hash_] == 0:
                return i-1
        return self.max
