# test query and delete throughput among CF, ShBF, VCF, QF, SFSM

import sys
import random
import math
import numpy as np
import time

sys.path.append("C:/Users/fptjy/pybloom")

from pybloom import BloomFilter
import bitarray, math, time
from utils import range_fn

sys.path.append("F:/Shifting_Filter/ShBF_ABF")
from ShBF_M import Shifting_BloomFilter_M

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter
from Vcuckoofilter14_7 import VCuckooFilter14_7

# sys.path.append("C:/Users/fptjy/Desktop/Quotient CF")
# from quotient_filter import QuotientFilter

sys.path.append("F:/Shifting_Filter/Shifting_Filter_on_slot/SVCF_Membership_3_hashes")
from SFS_M_3hash import SFSM_3hashes

mixlookup_thp_BF = []
mixlookup_thp_ShBFM = []
mixlookup_thp_CF = []
mixlookup_thp_VCF = []
# mixlookup_thp_QF = []
mixlookup_thp_SFSM = []

RESULT = []
RESULT.append("混合查询吞吐量vs空间占用率")

cishu = 30
print("测试次数为：", cishu)
RESULT.append("实验次数：" + str(cishu))

# 参数设置
alpha = 0.95
print("table occupancy:", alpha)
RESULT.append("所有Filter空间利用率固定为：" + str(alpha))

rate_array = np.arange(0.05, 1, 0.05)

RESULT.append("查询集合中存在元素所占比例：" + str(rate_array))

for cs in range(cishu):

    # 测试插入随机字符串
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
    testdata = [0 for i in range(2 ** 20)]
    for num in range(2 ** 20):
        sa = []
        for i in range(16):
            sa.append(random.choice(alphabet))
        testdata[num] = "".join(sa)

    testdata1 = [0 for i in range(2 ** 20)]
    for num in range(2 ** 20):
        sa = []
        for i in range(17):
            sa.append(random.choice(alphabet))
        testdata1[num] = "".join(sa)

    for ra in range(len(rate_array)):
        rate = rate_array[ra]
        print("fraction of queries on existing items:", rate)

        # 根据rate设置随机查询存在对象的数据集合testdata2
        datasize = int(alpha * len(testdata))
        exist_num = int(rate * datasize)
        testdata2 = [0 for i in range(datasize)]
        for i in range(exist_num):
            testdata2[i] = testdata[i]
        for i in range(exist_num, datasize):
            testdata2[i] = testdata1[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        # 先存储达到alpha时的一定数量的对象

        #BF
        f = BloomFilter(capacity=2 ** 20, error_rate=0.000015)
        for i in range(int(alpha * len(testdata))):
            f.add(testdata[i], skip_check=True)

        # ShBF
        ShBFM = Shifting_BloomFilter_M(k=12, m=int(2 ** 20 * 22.9), w=57)
        for i in range(int(alpha * len(testdata))):
            ShBFM.insert(testdata[i])

        CF = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19, max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            CF.insert(testdata[i])

        VCF = VCuckooFilter14_7(capacity=2 ** 18, bucket_size=4, fingerprint_size=20,
                                max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            VCF.insert(testdata[i])

        # QF = QuotientFilter()
        # for i in range(int(alpha * QF.p)):
        #     QF.addKey(testdata[i])

        SFSM = SFSM_3hashes(capacity=2 ** 18, bucket_size=4, fingerprint_size=18,
                            max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            SFSM.insert(testdata[i])

        # # 构造QF混合查询的数据集
        # QF_testdata2 = [0 for i in range(int(alpha * QF.p))]
        # for i in range(int(alpha * QF.p * rate)):
        #     QF_testdata2[i] = testdata[i]
        # for i in range(int(alpha * QF.p * rate), int(alpha * QF.p)):
        #     QF_testdata2[i] = testdata1[i]
        # state = np.random.get_state()
        # np.random.shuffle(QF_testdata2)
        # np.random.set_state(state)

        # 随机查一定比例存在的对象

        start = time.time()
        for i in range(len(testdata2)):
            f.__contains__(testdata2[i])
        end = time.time()
        mixlookup_thp_BF.append(len(testdata2) / (end - start))

        start = time.time()
        for i in range(len(testdata2)):
            ShBFM.query(testdata2[i])
        end = time.time()
        mixlookup_thp_ShBFM.append(len(testdata2) / (end - start))

        start = time.time()
        for i in range(len(testdata2)):
            CF.query(testdata2[i])
        end = time.time()
        mixlookup_thp_CF.append(len(testdata2) / (end - start))

        start = time.time()
        for i in range(len(testdata2)):
            VCF.query(testdata2[i])
        end = time.time()
        mixlookup_thp_VCF.append(len(testdata2) / (end - start))

        # start = time.time()
        # for i in range(len(QF_testdata2)):
        #     QF.lookup(testdata2[i])
        # end = time.time()
        # mixlookup_thp_QF.append(len(QF_testdata2) / (end - start))

        start = time.time()
        for i in range(len(testdata2)):
            SFSM.query(testdata2[i])
        end = time.time()
        mixlookup_thp_SFSM.append(len(testdata2) / (end - start))

mixlookup_thp_BF2 = [0 for i in range(19)]
mixlookup_thp_ShBFM2 = [0 for i in range(19)]
mixlookup_thp_CF2 = [0 for i in range(19)]
mixlookup_thp_VCF2 = [0 for i in range(19)]
# mixlookup_thp_QF2 = [0 for i in range(19)]
mixlookup_thp_SFSM2 = [0 for i in range(19)]

for j in range(19):
    k = j
    for i in range(cishu):
        mixlookup_thp_BF2[j] += mixlookup_thp_BF[k]
        mixlookup_thp_ShBFM2[j] += mixlookup_thp_ShBFM[k]
        mixlookup_thp_CF2[j] += mixlookup_thp_CF[k]
        mixlookup_thp_VCF2[j] += mixlookup_thp_VCF[k]
        # mixlookup_thp_QF2[j] += mixlookup_thp_QF[k]
        mixlookup_thp_SFSM2[j] += mixlookup_thp_SFSM[k]
        k += 19

for j in range(19):
    mixlookup_thp_BF2[j] = mixlookup_thp_BF2[j] / cishu
    mixlookup_thp_ShBFM2[j] = mixlookup_thp_ShBFM2[j] / cishu
    mixlookup_thp_CF2[j] = mixlookup_thp_CF2[j] / cishu
    mixlookup_thp_VCF2[j] = mixlookup_thp_VCF2[j] / cishu
    # mixlookup_thp_QF2[j] = mixlookup_thp_QF2[j] / cishu
    mixlookup_thp_SFSM2[j] = mixlookup_thp_SFSM2[j] / cishu

print("#############混合查询的实验结果###########")

print("mixlookup_thp_BF", mixlookup_thp_BF2)
print("mixlookup_thp_ShBFM", mixlookup_thp_ShBFM2)
print("mixlookup_thp_CF", mixlookup_thp_CF2)
print("mixlookup_thp_VCF", mixlookup_thp_VCF2)
# print("mixlookup_thp_QF", mixlookup_thp_QF2)
print("mixlookup_thp_SFSM", mixlookup_thp_SFSM2)

RESULT.append("mixlookup_thp_BF=" + str(mixlookup_thp_BF2))
RESULT.append("mixlookup_thp_ShBFM=" + str(mixlookup_thp_ShBFM2))
RESULT.append("mixlookup_thp_CF=" + str(mixlookup_thp_CF2))
RESULT.append("mixlookup_thp_VCF=" + str(mixlookup_thp_VCF2))
# RESULT.append("mixlookup_thp_QF=" + str(mixlookup_thp_QF2))
RESULT.append("mixlookup_thp_SFSM=" + str(mixlookup_thp_SFSM2))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Membership_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()

text_create("mixquery_thp_occupancy2", RESULT)