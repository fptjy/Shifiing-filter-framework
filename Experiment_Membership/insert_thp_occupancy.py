# test insertion throughput among CF, ShBF, VCF, QF, SFSM

import sys
import random
import math
import numpy as np
import time

sys.path.append("C:/Users/fptjy/pybloom")

from pybloom import BloomFilter
import bitarray, math, time
from utils import range_fn
import random

sys.path.append("F:/Shifting_Filter/ShBF_ABF")
from ShBF_M import Shifting_BloomFilter_M

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter
from Vcuckoofilter14_7 import VCuckooFilter14_7

sys.path.append("C:/Users/fptjy/Desktop/Quotient CF")
from quotient_filter import QuotientFilter

sys.path.append("F:/Shifting_Filter/Shifting_Filter_on_slot/SVCF_Membership_3_hashes")
from SFS_M_3hash import SFSM_3hashes


insert_thp_BF = []
insert_thp_ShBFM = []
insert_thp_CF = []
insert_thp_VCF = []
insert_thp_QF = []
insert_thp_SFSM = []

RESULT = []
RESULT.append("存储吞吐量vs空间占用率")

cishu = 30
print("测试次数为：", cishu)
RESULT.append("实验次数：" + str(cishu))

delta = 5000
print("general delta:", delta)


RESULT.append("测试步长（元素数量）：" + str(delta))

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

    # 参数设置并测试
    for alp in range(len(alpha_array)):

        alpha = alpha_array[alp]

        # 先存储达到alpha时的一定数量的对象
        # ShBF
        ShBFM = Shifting_BloomFilter_M(k=12, m=int(2 ** 20 * 22.9), w=57)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            ShBFM.insert(testdata[i])

        CF = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=19, max_displacements=500)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            CF.insert(testdata[i])

        VCF = VCuckooFilter14_7(capacity=2 ** 18, bucket_size=4, fingerprint_size=20,
                                max_displacements=500)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            VCF.insert(testdata[i])

        f = BloomFilter(capacity=2 ** 20, error_rate=0.000015)
        for i in range_fn(int(alpha * len(testdata) - delta / 2)):
            f.add(testdata[i], skip_check=True)

        # QF = QuotientFilter()
        # for i in range(int(alpha * QF.p - qf_delta / 2)):
        #     QF.addKey(testdata[i])

        SFSM = SFSM_3hashes(capacity=2 ** 18, bucket_size=4, fingerprint_size=18,
                            max_displacements=500)
        for i in range(int(alpha * len(testdata) - delta / 2)):
            SFSM.insert(testdata[i])

        # 开始测试达到alpha时，插入delta个对象的吞吐量
        start = time.time()
        for i in range(delta):
            ShBFM.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = time.time()
        time_consume = end - start
        if time_consume == 0:
            insert_thp_ShBFM.append(0)
        else:
            insert_thp_ShBFM.append(delta / (end - start))

        start = time.time()
        for i in range(delta):
            CF.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = time.time()
        time_consume = end - start
        if time_consume == 0:
            insert_thp_CF.append(0)
        else:
            insert_thp_CF.append(delta / (end - start))

        start = time.time()
        for i in range(delta):
            VCF.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = time.time()
        time_consume = end - start
        if time_consume == 0:
            insert_thp_VCF.append(0)
        else:
            insert_thp_VCF.append(delta / (end - start))


        start = time.time()
        for i in range(delta):
            f.add(testdata[int(alpha * len(testdata) - delta / 2) + i], skip_check=True)
        end = time.time()
        time_consume = end - start
        if time_consume == 0:
            insert_thp_BF.append(0)
        else:
            insert_thp_BF.append(delta / (end - start))

        # start = time.time()
        # for i in range(qf_delta):
        #     QF.addKey(testdata[int(alpha * QF.p - qf_delta / 2) + i])
        # end = time.time()
        # time_consume = end - start
        # if time_consume == 0:
        #     insert_thp_QF.append(0)
        # else:
        #     insert_thp_QF.append(qf_delta / (end - start))

        start = time.time()
        for i in range(delta):
            SFSM.insert(testdata[int(alpha * len(testdata) - delta / 2) + i])
        end = time.time()
        time_consume = end - start
        if time_consume == 0:
            insert_thp_SFSM.append(0)
        else:
            insert_thp_SFSM.append(delta / (end - start))

insert_thp_ShBFM2 = [0 for i in range(19)]
insert_thp_CF2 = [0 for i in range(19)]
insert_thp_VCF2 = [0 for i in range(19)]
# insert_thp_QF2 = [0 for i in range(19)]
insert_thp_SFSM2 = [0 for i in range(19)]
insert_thp_BF2 = [0 for i in range(19)]

for j in range(19):
    k = j
    for i in range(cishu):
        insert_thp_ShBFM2[j] += insert_thp_ShBFM[k]
        insert_thp_CF2[j] += insert_thp_CF[k]
        insert_thp_VCF2[j] += insert_thp_VCF[k]
        # insert_thp_QF2[j] += insert_thp_QF[k]
        insert_thp_SFSM2[j] += insert_thp_SFSM[k]
        insert_thp_BF2[j] += insert_thp_BF[k]
        k += 19

count_ShBFM = [0 for i in range(19)]
count_CF = [0 for i in range(19)]
count_VCF = [0 for i in range(19)]
# count_QF = [0 for i in range(19)]
count_SFSM = [0 for i in range(19)]
count_BF = [0 for i in range(19)]

for j in range(19):
    k = j
    for i in range(cishu):
        if insert_thp_ShBFM[k] == 0:
            count_ShBFM[j] += 1
        if insert_thp_CF[k] == 0:
            count_CF[j] += 1
        if insert_thp_VCF[k] == 0:
            count_VCF[j] += 1
        # if insert_thp_QF[k] == 0:
        #     count_QF[j] += 1
        if insert_thp_SFSM[k] == 0:
            count_SFSM[j] += 1
        if insert_thp_BF[k] == 0:
            count_BF[j] += 1
        k += 19

print("ShBFM中存储吞吐量中时间开销为0的次数", count_ShBFM)
print("CF中存储吞吐量中时间开销为0的次数", count_CF)
print("VCF中存储吞吐量中时间开销为0的次数", count_VCF)
# print("QF中存储吞吐量中时间开销为0的次数", count_QF)
print("SFSM中存储吞吐量中时间开销为0的次数", count_SFSM)
print("BF中存储吞吐量中时间开销为0的次数", count_BF)


RESULT.append("BF中存储吞吐量中时间开销为0的次数：" + str(count_BF))
RESULT.append("ShBFM中存储吞吐量中时间开销为0的次数：" + str(count_ShBFM))
RESULT.append("CF中存储吞吐量中时间开销为0的次数：" + str(count_CF))
RESULT.append("VCF中存储吞吐量中时间开销为0的次数：" + str(count_VCF))
# RESULT.append("QF中存储吞吐量中时间开销为0的次数：" + str(count_QF))
RESULT.append("SFSM中存储吞吐量中时间开销为0的次数：" + str(count_SFSM))


for j in range(19):
    insert_thp_ShBFM2[j] = insert_thp_ShBFM2[j] / (cishu - count_ShBFM[j])
    insert_thp_CF2[j] = insert_thp_CF2[j] / (cishu - count_CF[j])
    insert_thp_VCF2[j] = insert_thp_VCF2[j] / (cishu - count_VCF[j])
    # insert_thp_QF2[j] = insert_thp_QF2[j] / (cishu - count_QF[j])
    insert_thp_SFSM2[j] = insert_thp_SFSM2[j] / (cishu - count_SFSM[j])
    insert_thp_BF2[j] = insert_thp_BF2[j] / (cishu - count_BF[j])

print("##############实验结果###############")
print("insert_thp_BF", insert_thp_BF2)
print("insert_thp_ShBFM", insert_thp_ShBFM2)
print("insert_thp_CF", insert_thp_CF2)
print("insert_thp_VCF", insert_thp_VCF2)
# print("insert_thp_QF", insert_thp_QF2)
print("insert_thp_SFSM", insert_thp_SFSM2)


RESULT.append("insert_thp_BF =" + str(insert_thp_BF2))
RESULT.append("insert_thp_ShBFM =" + str(insert_thp_ShBFM2))
RESULT.append("insert_thp_CF =" + str(insert_thp_CF2))
RESULT.append("insert_thp_VCF =" + str(insert_thp_VCF2))
# RESULT.append("insert_thp_QF =" + str(insert_thp_QF2))
RESULT.append("insert_thp_SFSM =" + str(insert_thp_SFSM2))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Membership_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("insert_thp_occupancy2", RESULT)
