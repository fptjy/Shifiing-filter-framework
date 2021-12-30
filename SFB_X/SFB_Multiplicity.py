"""
Shifting Filter
"""

import random

import bucket_SFBX  # 相对导入from . import bucket这种导入方式会报错
import exceptions
import hashutils_DJBhash
from mmh3 import hash as m3h


class SFB_X(object):
    """
    Cuckoo Filter class.

    Implements insert, delete and contains operations for the filter.
    """

    def __init__(self, capacity, bucket_size=4, fingerprint_size=16, block_number=2 ** 5,
                 max_displacements=500):
        """
        Initialize CuckooFilter object.

        :param capacity: Size of the Cuckoo Filter
        :param bucket_size: Number of entries in a bucket
        :param fingerprint_size: Fingerprint size in bytes
        :param max_displacements: Maximum number of evictions before filter is
        considered full
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_displacements = max_displacements
        self.block_number = block_number
        self.block_capacity = int(self.capacity / self.block_number)
        self.buckets = [bucket_SFBX.Bucket(size=bucket_size)
                        for _ in range(self.capacity)]
        self.size = 0
        # self.kicks = 0  #自己写的，用来获取踢出重放次数

    def __repr__(self):  # 重写__repr__()，定义打印class的信息
        return '<CuckooFilter: capacity=' + str(self.capacity) + \
               ', size=' + str(self.size) + ', fingerprint size=' + \
               str(self.fingerprint_size) + ' byte(s)>'

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return self.contains(item)

    def _get_index(self, item):
        index = hashutils_DJBhash.hash_code(item) % self.block_capacity
        return index

    def _get_alternate_index(self, index, fingerprint):
        alt_index = (index ^ hashutils_DJBhash.hash_code(fingerprint)) % self.block_capacity
        return alt_index

    def insert(self, item, counter):
        """
        Insert an item into the filter.

        :param item: Item to be inserted.
        :return: True if insert is successful; CuckooFilterFullException if
        filter is full.
        """
        fingerprint = hashutils_DJBhash.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)
        count = counter - 1
        count_input = count // self.block_number
        block = (m3h(item, 1) % self.block_number + count % self.block_number) % self.block_number

        delta = block * self.block_capacity
        i = i + delta
        j = j + delta

        if self.buckets[i].insert(fingerprint, count_input) \
                or self.buckets[j].insert(fingerprint, count_input):
            self.size += 1
            return True

        eviction_index = random.choice([i, j])
        for _ in range(self.max_displacements):
            f = self.buckets[eviction_index].swap(fingerprint, count_input)
            eviction_index = self._get_alternate_index(eviction_index - delta, f[0]) + delta
            if self.buckets[eviction_index].insert(f[0], f[1]):
                self.size += 1
                return True
            fingerprint = f[0]
            count_input = f[1]
        # Filter is full
        return self.size

        # raise exceptions.CuckooFilterFullException('Insert operation failed. '
        #                                           'Filter is full.')

    def query(self, item):
        """
        Check if the filter contains the item.

        :param item: Item to check its presence in the filter.
        :return: True, if item is in the filter; False, otherwise.
        """
        fingerprint = hashutils_DJBhash.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)
        initial = m3h(item, 1) % self.block_number

        for number in range(self.block_number):
            delta = number * self.block_capacity
            for slot in range(self.bucket_size):
                if self.buckets[i + delta].bucket[slot][0] == fingerprint:
                    return self.buckets[i + delta].bucket[slot][1] * self.block_number + self.compute_delta(
                        location=initial, current=number)

                if self.buckets[j + delta].bucket[slot][0] == fingerprint:
                    return self.buckets[j + delta].bucket[slot][1] * self.block_number + self.compute_delta(
                        location=initial, current=number)

        return False

    def compute_delta(self, location, current):
        if current < location:
            return current + self.block_number - location + 1
        else:
            return current - location + 1

    def delete(self, item):
        """
        Delete an item from the filter.

        To delete an item safely, it must have been previously inserted.
        Otherwise, deleting a non-inserted item might unintentionally remove
        a real, different item that happens to share the same fingerprint.

        :param item: Item to delete from the filter.
        :return: True, if item is found and deleted; False, otherwise.
        """
        fingerprint = hashutils_DJBhash.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate_index(i, fingerprint)

        for number in range(self.block_number):
            delta = number * self.block_capacity
            if self.buckets[i + delta].delete(fingerprint) or self.buckets[j + delta].delete(fingerprint):
                self.size -= 1
                return True

        return False
