import random
import numpy as np
import time
import sys

sys.path.append(r"F:/Shifting_Filter/Shifting_Filter_on_slot/SVCF_Membership_3_hashes")
from svcf_3hashes import ShiftingVerticalCuckooFilter_3hashes

sys.path.append(r"F:/Shifting_Filter/Shifting_Filter_on_bucket/SF_on_bucket")
from sf_bucket_direction import ShiftingFilterB

l = [i for i in range(1, 25)]
m = [2 ** 14, 2 ** 16, 2 ** 18, 2 ** 20]
b = 4
n = [b * i for i in m]
print(l)
print(m)
print(n)

cishu = 10

result_SFS = [[] for i in range(4)]
result_SFB = [[] for i in range(4)]

for mm in range(len(m)):

    for ll in range(len(l)):

        x = []
        y = []
        for cs in range(cishu):

            # 测试插入随机字符串
            alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
            testdata = [0 for _ in range(n[mm])]
            for num in range(n[mm]):
                sa = []
                for i in range(16):
                    sa.append(random.choice(alphabet))
                testdata[num] = "".join(sa)

            SFS = ShiftingVerticalCuckooFilter_3hashes(capacity=m[mm], bucket_size=b, fingerprint_size=l[ll],
                                                       max_displacements=500)

            SFB = ShiftingFilterB(capacity=m[mm], bucket_size=b, fingerprint_size=l[ll], block_number=2 ** 5,
                                  max_displacements=500)

            # recording the load factor of SFS
            i = 0
            while True:
                if SFS.insert(testdata[i]) != True:
                    break
                i += 1
            x.append(SFS.size / (SFS.capacity * SFS.bucket_size))

            # recording the load factor of SFB
            i = 0
            while True:
                if SFB.insert(testdata[i]) != True:
                    break
                i += 1
            y.append(SFB.size / (SFB.capacity * SFB.bucket_size))

        result_SFS[mm].append(np.mean(x))
        result_SFB[mm].append(np.mean(y))

RESULT = []
RESULT.append("实验次数：" + str(cishu))
RESULT.append("bucket number m=" + str(m))
RESULT.append("fingerprint size l=" + str(l))
RESULT.append("bucket size b=" + str(b))
RESULT.append("SFS")
RESULT.append(str(result_SFS))
RESULT.append("SFB")
RESULT.append("the block number of SFB" + str(2 ** 5))
RESULT.append(str(result_SFB))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Load_factor/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("load_factor_SFS_B", RESULT)
