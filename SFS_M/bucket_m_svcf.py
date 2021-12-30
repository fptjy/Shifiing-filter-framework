class Bucket(object):

    def __init__(self, size=4):
        self.size = size
        self.bucket = [-1 for i in range(self.size)]

    def __repr__(self):
        return '<Bucket: ' + str(self.bucket) + '>'

    def __contains__(self, item):
        return item in self.bucket

    def __len__(self):
        return len(self.bucket)

    def insert(self, item, location):
        """
        Insert a fingerprint into the bucket
        :param item:
        :return:
        """
        if self.bucket[location] == -1:
            self.bucket[location] = item
            return True
        return False

    def delete(self, item, location):
        """
        Delete a fingerprint from the bucket.
        :param item:
        :return:
        """
        if self.bucket[location] == item:
            self.bucket[location] = -1
            return True
        return False

    def swap(self, finger, location):
        """
        Swap fingerprint with a random entry stored in the bucket and return
        the swapped fingerprint
        :param finger:
        :return:
        """
        swapped_item = self.bucket[location]
        self.bucket[location] = finger
        return swapped_item
