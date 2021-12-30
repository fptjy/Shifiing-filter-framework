class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = [[-1, 0] for _ in range(self.size)]

    def __repr__(self):
        return '<Bucket: ' + str(self.bucket) + '>'

    def __contains__(self, item):
        return item in self.bucket

    def __len__(self):
        return len(self.bucket)

    def insert(self, item, mark, location):
        """
        Insert a fingerprint into the bucket
        :param item:
        :param mark: eg, mark= [1,2] for two set.
        :return:
        """
        if self.bucket[location][0] == -1:
            self.bucket[location][0] = item
            self.bucket[location][1] = mark
            return True
        return False

    def delete(self, item, location):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        if self.bucket[location][0] == item:
            self.bucket[location][1] = 0
            return True
        return False

    def delete2(self, item, mark, location):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        if mark[0] == 0:
            return False
        if self.bucket[location][0] == item:
            for mb in mark:
                self.bucket[location][1] = self.bucket[location][1] ^ mb
            if self.bucket[location][1] == 0:
                self.bucket[location][0] = -1
            return True
        return False

    def swap(self, finger, mark, location):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param finger:
        :return:
        """
        swapped_item = self.bucket[location]
        self.bucket[location] = [finger, mark]
        return swapped_item
