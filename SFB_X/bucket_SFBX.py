import random


class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = [[-1, 0] for i in range(self.size)]

    def __repr__(self):
        return '<Bucket: ' + str(self.bucket) + '>'

    def __contains__(self, item):
        return item in self.bucket

    def __len__(self):
        return len(self.bucket)

    def insert(self, item, auxiliary):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        try:
            self.bucket[self.bucket.index([-1, 0])] = [item, auxiliary]
            return True
        except ValueError:
            return False

    def delete(self, item):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        for i in range(self.size):
            if self.bucket[i][0] == item:
                self.bucket[i] = [-1, 0]
                return True
        return False

    # def lookup(self, item):
    #     """
    #     Delete a fingerprint from the bucket.
    #     :param item:
    #     :return:
    #     """
    #     for i in range(self.size):
    #         if self.bucket[i][0] == item:
    #             return True
    #     return False

    def is_not_full(self):
        return [-1, 0] in self.bucket

    def swap(self, item, auxiliary):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param item:
        :return:
        """
        index = random.choice(range(len(self.bucket)))  # 从桶中四个槽中随机选一个
        swapped_item = self.bucket[index]
        self.bucket[index] = [item, auxiliary]
        return swapped_item
