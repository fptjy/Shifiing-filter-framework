"""
Shifting Cuckoo Filter
"""

import random
import bucket_SFSX  # 相对导入from . import bucket这种导入方式会报错
import exceptions
import hashutils_DJBhash


class SFS_X(object):
    """
    Shifting Cuckoo Filter class.

    Implements insert, delete and contains operations for the filter.
    """

    def __init__(self, capacity, bucket_size=4, fingerprint_size=16,
                 max_displacements=50):
        """
        Initialize ShiftingCuckooFilter object.

        :param capacity: Size of the Shifting Cuckoo Filter
        :param bucket_size: Number of entries in a bucket
        :param fingerprint_size: Fingerprint size
        :param max_displacements: Maximum number of evictions before filter is
        considered full
        """
        self.capacity = capacity
        self.bucket_size = bucket_size
        self.fingerprint_size = fingerprint_size
        self.max_displacements = max_displacements
        self.buckets = [bucket_SFSX.Bucket(size=bucket_size)
                        for _ in range(self.capacity)]
        self.size = 0
        # self.kicks = 0

    def __repr__(self):  # 重写__repr__()，定义打印class的信息
        return '<CuckooFilter: capacity=' + str(self.capacity) + \
               ', size=' + str(self.size) + ', fingerprint size=' + \
               str(self.fingerprint_size) + ' byte(s)>'

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return self.query(item)

    def _get_index(self, item):
        index = hashutils_DJBhash.hash_code(item) % self.capacity
        return index

    def _get_alternate1_index(self, index, fingerprint):
        alt_index1 = (index ^ (hashutils_DJBhash.hash_code(fingerprint) & 0b0101010101010101)) % self.capacity
        return alt_index1

    def _get_alternate2_index(self, index, fingerprint):
        alt_index2 = (index ^ (hashutils_DJBhash.hash_code(fingerprint) & 0b1010101010101010)) % self.capacity
        return alt_index2

    def _get_alternate3_index(self, index, fingerprint):
        alt_index3 = (index ^ hashutils_DJBhash.hash_code(fingerprint)) % self.capacity
        return alt_index3

    def insert(self, item, count):
        """
        Insert an item into the filter.

        :param item: Item to be inserted.
        :return: True if insert is successful; ShiftingCuckooFilterFullException if
        filter is full.
        """
        fingerprint = hashutils_DJBhash.fingerprint(item, self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate1_index(i, fingerprint)
        x = self._get_alternate2_index(i, fingerprint)
        y = self._get_alternate3_index(i, fingerprint)

        count1 = count - 1
        count_input = count1 // self.bucket_size
        Locate = (fingerprint % self.bucket_size + count1 % self.bucket_size) % self.bucket_size

        if self.buckets[i].insert(item=fingerprint, auxiliary=count_input, location=Locate):
            self.size += 1
            return True
        if self.buckets[y].insert(item=fingerprint, auxiliary=count_input, location=Locate):
            self.size += 1
            return True
        if self.buckets[j].insert(item=fingerprint, auxiliary=count_input, location=Locate):
            self.size += 1
            return True
        if self.buckets[x].insert(item=fingerprint, auxiliary=count_input, location=Locate):
            self.size += 1
            return True

        eviction_index = random.choice([i, j, x, y])

        for _ in range(self.max_displacements):
            f = self.buckets[eviction_index].swap(finger=fingerprint, counter=count_input,
                                                  location=Locate)
            eviction_index1 = self._get_alternate1_index(eviction_index, f[0])
            eviction_index2 = self._get_alternate2_index(eviction_index, f[0])
            eviction_index3 = self._get_alternate3_index(eviction_index, f[0])

            if self.buckets[eviction_index3].insert(item=f[0], auxiliary=f[1], location=Locate):
                self.size += 1
                return True
            if self.buckets[eviction_index1].insert(item=f[0], auxiliary=f[1], location=Locate):
                self.size += 1
                return True
            if self.buckets[eviction_index2].insert(item=f[0], auxiliary=f[1], location=Locate):
                self.size += 1
                return True
            eviction_index = random.choice([eviction_index1, eviction_index2, eviction_index3])
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
        j = self._get_alternate1_index(i, fingerprint)
        x = self._get_alternate2_index(i, fingerprint)
        y = self._get_alternate3_index(i, fingerprint)

        for number in range(self.bucket_size):
            if self.buckets[i].bucket[number][0] == fingerprint:
                return self.buckets[i].bucket[number][1] * self.bucket_size + self.compute_delta(
                    location=fingerprint % self.bucket_size, current=number)
            if self.buckets[j].bucket[number][0] == fingerprint:
                return self.buckets[j].bucket[number][1] * self.bucket_size + self.compute_delta(
                    location=fingerprint % self.bucket_size, current=number)
            if self.buckets[x].bucket[number][0] == fingerprint:
                return self.buckets[x].bucket[number][1] * self.bucket_size + self.compute_delta(
                    location=fingerprint % self.bucket_size, current=number)
            if self.buckets[y].bucket[number][0] == fingerprint:
                return self.buckets[y].bucket[number][1] * self.bucket_size + self.compute_delta(
                    location=fingerprint % self.bucket_size, current=number)
        return False

    def compute_delta(self, location, current):
        if current < location:
            return current + self.bucket_size - location + 1
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
        fingerprint = hashutils_DJBhash.fingerprint(item, size=self.fingerprint_size)
        i = self._get_index(item)
        j = self._get_alternate1_index(i, fingerprint)
        x = self._get_alternate2_index(i, fingerprint)
        y = self._get_alternate3_index(i, fingerprint)

        if self.buckets[i].delete(fingerprint):
            self.size -= 1
            return True
        if self.buckets[j].delete(fingerprint):
            self.size -= 1
            return True
        if self.buckets[x].delete(fingerprint):
            self.size -= 1
            return True
        if self.buckets[y].delete(fingerprint):
            self.size -= 1
            return True
        return False
