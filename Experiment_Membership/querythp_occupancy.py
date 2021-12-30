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

sys.path.append("C:/Users/fptjy/Desktop/Quotient CF")
from quotient_filter import QuotientFilter

sys.path.append("F:/Shifting_Filter/Shifting_Filter_on_slot/SVCF_Membership_3_hashes")
from SFS_M_3hash import SFSM_3hashes

negative_lookup_thp_BF = []
negative_lookup_thp_ShBFM = []
negative_lookup_thp_CF = []
negative_lookup_thp_VCF = []
# negative_lookup_thp_QF = []
negative_lookup_thp_SFSM = []

positive_lookup_thp_BF = []
positive_lookup_thp_ShBFM = []
positive_lookup_thp_CF = []
positive_lookup_thp_VCF = []
# positive_lookup_thp_QF = []
positive_lookup_thp_SFSM = []

delete_thp_BF = []
delete_thp_CF = []
delete_thp_VCF = []
# delete_thp_QF = []
delete_thp_SFSM = []

RESULT = []
RESULT.append("查询吞吐量（positive和negative）vs空间占用率")

cishu = 30
print("测试次数为：", cishu)
RESULT.append("实验次数：" + str(cishu))

alpha_array = np.arange(0.05, 1, 0.05)
RESULT.append("测试的空间利用率所在点：" + str(alpha_array))

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

    # 参数设置并测试
    for alp in range(len(alpha_array)):

        alpha = alpha_array[alp]

        # 设置随机查询存在对象的数据集合
        datasize = int(alpha * len(testdata))
        testdata2 = [0 for i in range(datasize)]
        for i in range(datasize):
            testdata2[i] = testdata[i]
        state = np.random.get_state()
        np.random.shuffle(testdata2)
        np.random.set_state(state)

        # 先存储达到alpha时的一定数量的对象
        # BF
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

        ### 开始测试达到alpha时，查询和删除的吞吐量
        ## 测试BF
        # 查不存在的对象
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            f.__contains__(testdata1[i])
        end = time.time()
        time_consume = end - start
        negative_lookup_thp_BF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = time.time()
        for i in range(len(testdata2)):
            f.__contains__(testdata2[i])
        end = time.time()
        time_consume = end - start
        positive_lookup_thp_BF.append(len(testdata2) / time_consume)

        ## 测试ShBFM
        # 查不存在的对象
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            ShBFM.query(testdata1[i])
        end = time.time()
        time_consume = end - start
        negative_lookup_thp_ShBFM.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = time.time()
        for i in range(len(testdata2)):
            ShBFM.query(testdata2[i])
        end = time.time()
        time_consume = end - start
        positive_lookup_thp_ShBFM.append(len(testdata2) / time_consume)

        ## 测试CF
        # 查不存在的对象
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            CF.query(testdata1[i])
        end = time.time()
        time_consume = end - start
        negative_lookup_thp_CF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = time.time()
        for i in range(len(testdata2)):
            CF.query(testdata2[i])
        end = time.time()
        time_consume = end - start
        positive_lookup_thp_CF.append(len(testdata2) / time_consume)

        # # 删除对象测试
        # start = time.time()
        # for i in range(len(testdata2)):
        #     CF.delete(testdata2[i])
        # end = time.time()
        # time_consume = end - start
        # delete_thp_CF.append(len(testdata2) / time_consume)

        ## 测试VCF
        # 查不存在的对象
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            VCF.query(testdata1[i])
        end = time.time()
        time_consume = end - start
        negative_lookup_thp_VCF.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = time.time()
        for i in range(len(testdata2)):
            VCF.query(testdata2[i])
        end = time.time()
        time_consume = end - start
        positive_lookup_thp_VCF.append(len(testdata2) / time_consume)

        # # 删除对象测试
        # start = time.time()
        # for i in range(len(testdata2)):
        #     VCF.delete(testdata2[i])
        # end = time.time()
        # time_consume = end - start
        # delete_thp_VCF.append(len(testdata2) / time_consume)

        # ## 测试QF
        # # 查不存在的对象
        # start = time.time()
        # for i in range(int(alpha * len(testdata1))):
        #     QF.lookup(testdata1[i])
        # end = time.time()
        # time_consume = end - start
        # negative_lookup_thp_QF.append(int(alpha * len(testdata1)) / time_consume)
        #
        # # 随机查存在的对象
        # start = time.time()
        # for i in range(len(testdata2)):
        #     QF.lookup(testdata2[i])
        # end = time.time()
        # time_consume = end - start
        # positive_lookup_thp_QF.append(len(testdata2) / time_consume)
        #
        # # 删除对象测试
        # start = time.time()
        # for i in range(len(testdata2)):
        #     QF.delete(testdata2[i])
        # end = time.time()
        # time_consume = end - start
        #
        # if time_consume == 0:
        #     delete_thp_QF.append(0)
        # else:
        #     delete_thp_QF.append(len(testdata2) / time_consume)

        ## 测试SFSM
        # 查不存在的对象
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            SFSM.query(testdata1[i])
        end = time.time()
        time_consume = end - start
        negative_lookup_thp_SFSM.append(int(alpha * len(testdata1)) / time_consume)

        # 随机查存在的对象
        start = time.time()
        for i in range(len(testdata2)):
            SFSM.query(testdata2[i])
        end = time.time()
        time_consume = end - start
        positive_lookup_thp_SFSM.append(len(testdata2) / time_consume)

        # # 删除对象测试
        # start = time.time()
        # for i in range(len(testdata2)):
        #     SFSM.delete(testdata2[i])
        # end = time.time()
        # time_consume = end - start
        # delete_thp_SFSM.append(len(testdata2) / time_consume)

negative_lookup_thp_BF2 = [0 for i in range(19)]
negative_lookup_thp_ShBFM2 = [0 for i in range(19)]
negative_lookup_thp_CF2 = [0 for i in range(19)]
negative_lookup_thp_VCF2 = [0 for i in range(19)]
# negative_lookup_thp_QF2 = [0 for i in range(19)]
negative_lookup_thp_SFSM2 = [0 for i in range(19)]

positive_lookup_thp_BF2 = [0 for i in range(19)]
positive_lookup_thp_ShBFM2 = [0 for i in range(19)]
positive_lookup_thp_CF2 = [0 for i in range(19)]
positive_lookup_thp_VCF2 = [0 for i in range(19)]
# positive_lookup_thp_QF2 = [0 for i in range(19)]
positive_lookup_thp_SFSM2 = [0 for i in range(19)]

# delete_thp_CF2 = [0 for i in range(19)]
# delete_thp_VCF2 = [0 for i in range(19)]
# # delete_thp_QF2 = [0 for i in range(19)]
# delete_thp_SFSM2 = [0 for i in range(19)]

for j in range(19):
    k = j
    for i in range(cishu):
        negative_lookup_thp_BF2[j] += negative_lookup_thp_BF[k]
        negative_lookup_thp_ShBFM2[j] += negative_lookup_thp_ShBFM[k]
        negative_lookup_thp_CF2[j] += negative_lookup_thp_CF[k]
        negative_lookup_thp_VCF2[j] += negative_lookup_thp_VCF[k]
        # negative_lookup_thp_QF2[j] += negative_lookup_thp_QF[k]
        negative_lookup_thp_SFSM2[j] += negative_lookup_thp_SFSM[k]

        positive_lookup_thp_BF2[j] += positive_lookup_thp_BF[k]
        positive_lookup_thp_ShBFM2[j] += positive_lookup_thp_ShBFM[k]
        positive_lookup_thp_CF2[j] += positive_lookup_thp_CF[k]
        positive_lookup_thp_VCF2[j] += positive_lookup_thp_VCF[k]
        # positive_lookup_thp_QF2[j] += positive_lookup_thp_QF[k]
        positive_lookup_thp_SFSM2[j] += positive_lookup_thp_SFSM[k]

        # delete_thp_CF2[j] += delete_thp_CF[k]
        # delete_thp_VCF2[j] += delete_thp_VCF[k]
        # # delete_thp_QF2[j] += delete_thp_QF[k]
        # delete_thp_SFSM2[j] += delete_thp_SFSM[k]
        k += 19

# count = [0 for i in range(19)]
# for j in range(19):
#     k = j
#     for i in range(cishu):
#         if delete_thp_QF[k] == 0:
#             count[j] += 1
#             k += 19

# print("count为：", count)
# RESULT.append("Quotient filter删除时时间开销为0的次数：" + str(count))

for i in range(19):
    negative_lookup_thp_BF2[i] = negative_lookup_thp_BF2[i] / cishu
    negative_lookup_thp_ShBFM2[i] = negative_lookup_thp_ShBFM2[i] / cishu
    negative_lookup_thp_CF2[i] = negative_lookup_thp_CF2[i] / cishu
    negative_lookup_thp_VCF2[i] = negative_lookup_thp_VCF2[i] / cishu
    # negative_lookup_thp_QF2[i] = negative_lookup_thp_QF2[i] / cishu
    negative_lookup_thp_SFSM2[i] = negative_lookup_thp_SFSM2[i] / cishu

    positive_lookup_thp_BF2[i] = positive_lookup_thp_BF2[i] / cishu
    positive_lookup_thp_ShBFM2[i] = positive_lookup_thp_ShBFM2[i] / cishu
    positive_lookup_thp_CF2[i] = positive_lookup_thp_CF2[i] / cishu
    positive_lookup_thp_VCF2[i] = positive_lookup_thp_VCF2[i] / cishu
    # positive_lookup_thp_QF2[i] = positive_lookup_thp_QF2[i] / cishu
    positive_lookup_thp_SFSM2[i] = positive_lookup_thp_SFSM2[i] / cishu

    # delete_thp_CF2[i] = delete_thp_CF2[i] / cishu
    # delete_thp_VCF2[i] = delete_thp_VCF2[i] / cishu
    # # delete_thp_QF2[i] = delete_thp_QF2[i] / (cishu - count[i])
    # delete_thp_SFSM2[i] = delete_thp_SFSM2[i] / cishu

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

print("打印实验结果")
print("negative_lookup_BF", negative_lookup_thp_BF2)
print("negative_lookup_ShBFM", negative_lookup_thp_ShBFM2)
print("negative_lookup_CF", negative_lookup_thp_CF2)
print("negative_lookup_VCF", negative_lookup_thp_VCF2)
# print("negative_lookup_QF", negative_lookup_thp_QF2)
print("negative_lookup_SFSM", negative_lookup_thp_SFSM2)

RESULT.append("negative_lookup_BF=" + str(negative_lookup_thp_BF2))
RESULT.append("negative_lookup_ShBFM=" + str(negative_lookup_thp_ShBFM2))
RESULT.append("negative_lookup_CF=" + str(negative_lookup_thp_CF2))
RESULT.append("negative_lookup_VCF=" + str(negative_lookup_thp_VCF2))
# RESULT.append("negative_lookup_QF=" + str(negative_lookup_thp_QF2))
RESULT.append("negative_lookup_SFSM=" + str(negative_lookup_thp_SFSM2))

print("positive_lookup_BF", positive_lookup_thp_BF2)
print("positive_lookup_ShBFM", positive_lookup_thp_ShBFM2)
print("positive_lookup_CF", positive_lookup_thp_CF2)
print("positive_lookup_VCF", positive_lookup_thp_VCF2)
# print("positive_lookup_QF", positive_lookup_thp_QF2)
print("positive_lookup_SFSM", positive_lookup_thp_SFSM2)

RESULT.append("positive_lookup_BF=" + str(positive_lookup_thp_BF2))
RESULT.append("positive_lookup_ShBFM=" + str(positive_lookup_thp_ShBFM2))
RESULT.append("positive_lookup_CF=" + str(positive_lookup_thp_CF2))
RESULT.append("positive_lookup_VCF=" + str(positive_lookup_thp_VCF2))
# RESULT.append("positive_lookup_QF=" + str(positive_lookup_thp_QF2))
RESULT.append("positive_lookup_SFSM=" + str(positive_lookup_thp_SFSM2))

# print("delete_CF", delete_thp_CF2)
# print("delete_VCF", delete_thp_VCF2)
# # print("delete_QF", delete_thp_QF2)
# print("delete_SFSM", delete_thp_SFSM2)
#
# RESULT.append("delete_CF=" + str(delete_thp_CF2))
# RESULT.append("delete_VCF=" + str(delete_thp_VCF2))
# # RESULT.append("delete_QF=" + str(delete_thp_QF2))
# RESULT.append("delete_SFSM=" + str(delete_thp_SFSM2))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Membership_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()

text_create("query_delete_thp_occupancy2", RESULT)
