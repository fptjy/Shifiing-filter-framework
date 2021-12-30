# test among ShBF, SFSA

import sys
import random
import math
import numpy as np
import time

sys.path.append("F:/Shifting_Filter/ShBF_ABF")
from ShBF_A import Shifting_BloomFilter_A

sys.path.append("F:/Shifting_Filter/SFS_Association")
from SFS_AssociationQuery import SFS_A

sys.path.append("C:/Users/fptjy/pydaima/cuckoopy-master/cuckoopy")
from cuckoofilter import CuckooFilter

RESULT = []
RESULT.append("性能 vs O分数（存两个集合，查三个集合，包括不存储在集合中的元素）")

cishu = 30
print("测试次数为：", cishu)
RESULT.append("实验次数：" + str(cishu))

# 存储集合，这里两个集合S1和S2
S = [1, 2, 12]
# s2 = [1, 2, 3, 12, 13, 23, 123]
# s3 = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]

# Rate = [[0.5, 0.5, 0], [0.4, 0.4, 0.2], [0.3, 0.3, 0.4], [0.2, 0.2, 0.6], [0.1, 0.1, 0.8], [0, 0, 1]]
# Rate_query = [[1, 0, 0, 0], [0.7, 0.1, 0.1, 0.1], [0.5, 0.1, 0.1, 0.3], [0.3, 0.1, 0.1, 0.5], [0.1, 0.1, 0.1, 0.7],
#               [0, 0, 0, 1]]

Rate = [[0.5, 0.5, 0], [0.4, 0.4, 0.2], [0.3, 0.3, 0.4], [0.2, 0.2, 0.6], [0.1, 0.1, 0.8], [0, 0, 1]]
Rate_query = [[1, 0, 0, 0], [0.7, 0.1, 0.1, 0.1], [0.3, 0.3, 0.3, 0.1], [0.25, 0.15, 0.15, 0.45], [0.1, 0.1, 0.1, 0.7],
              [0, 0, 0, 1]]

# Rate = [[0.3, 0.3, 0.4]]
# Rate_query = [[0.5, 0.1, 0.1, 0.3]]

O_score = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
RESULT.append("自变量O分数的范围：" + str(O_score))

RESULT.append("ShBFA设计：" + "ShBFA = Shifting_BloomFilter_A(k=12, m=int(2 ** 20 * 18), w=57, sets=S)")
RESULT.append(
    "SFSA设计：" + "SFSA = SFS_A(capacity=2 ** 18, bucket_size=4, markbits=2, fingerprint_size=16,max_displacements=500)")

alpha = 0.95
N = int(alpha * 2 ** 20)

RESULT.append("空间利用率：" + str(alpha))

insert_thp_SFSA = []
insert_thp_ShBFA = []

query_thp_SFSA = []
query_thp_ShBFA = []

delete_thp_SFSA = []

precision_SFSA = []
precision_ShBFA = []

for r in range(len(Rate)):
    insert_thp_SFSA2 = []
    insert_thp_ShBFA2 = []

    query_thp_SFSA2 = []
    query_thp_ShBFA2 = []

    delete_thp_SFSA2 = []

    precision_SFSA2 = []
    precision_ShBFA2 = []

    for cs in range(cishu):
        n1 = int(N * Rate[r][0])
        n2 = int(N * Rate[r][1])
        n12 = int(N * Rate[r][2])

        # two CFs for set1 and set2
        CF1 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)
        CF2 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)

        # creat test datasets
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        # creat set1
        set1 = [0 for i in range(n1)]
        for num in range(n1):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set1[num] = "".join(sa)
        for i in range(len(set1)):
            CF1.insert(set1[i])

        # creat set2
        set2 = [0 for i in range(n2)]
        for num in range(n2):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set2[num] = "".join(sa)
        for i in range(len(set2)):
            CF2.insert(set2[i])

        # creat set12
        set12 = [0 for i in range(n12)]
        for num in range(n12):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set12[num] = "".join(sa)
        for i in range(len(set12)):
            CF1.insert(set12[i])
        for i in range(len(set12)):
            CF2.insert(set12[i])

        ShBFA = Shifting_BloomFilter_A(k=12, m=int(2 ** 20 * 18), w=57, sets=S)
        SFSA = SFS_A(capacity=2 ** 18, bucket_size=4, fingerprint_size=16,
                     max_displacements=500)

        ## test of insertion throughput
        # ShBFA存储
        start = time.time()
        for i in range(len(set1)):
            CF1.query(set1[i])
            CF2.query(set1[i])
            ShBFA.insert(content=set1[i], mark=[1])
        for i in range(len(set2)):
            CF1.query(set2[i])
            CF2.query(set2[i])
            ShBFA.insert(content=set2[i], mark=[2])
        for i in range(len(set12)):
            CF1.query(set12[i])
            CF2.query(set12[i])
            ShBFA.insert(content=set12[i], mark=[1, 2])
        end = time.time()
        time_consume = end - start
        insert_thp_ShBFA2.append(N / time_consume)

        # SFSA存储
        start = time.time()
        for i in range(len(set1)):
            SFSA.insert(item=set1[i], Mark=1)
        for i in range(len(set2)):
            SFSA.insert(item=set2[i], Mark=2)
        for i in range(len(set12)):
            SFSA.insert(item=set12[i], Mark=3)
        end = time.time()
        time_consume = end - start
        insert_thp_SFSA2.append(N / time_consume)

        # creat query sets
        nq0 = int(N * Rate_query[r][0])
        nq1 = int(N * Rate_query[r][1])
        nq2 = int(N * Rate_query[r][2])
        nq12 = int(N * Rate_query[r][3])

        # creat test datasets
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        # creat set_query0
        set_query0 = [0 for i in range(nq0)]
        for num in range(nq0):
            sa = []
            for i in range(17):
                sa.append(random.choice(alphabet))
            set_query0[num] = "".join(sa)

        ##test of query throughput
        # test of ShBFA
        start = time.time()
        for i in range(nq0):
            ShBFA.query(set_query0[i])
        for i in range(nq1):
            ShBFA.query(set1[i])
        for i in range(nq2):
            ShBFA.query(set2[i])
        for i in range(nq12):
            ShBFA.query(set12[i])
        end = time.time()
        time_consume = end - start
        query_thp_ShBFA2.append(N / time_consume)

        # test of SFSA
        start = time.time()
        for i in range(nq0):
            SFSA.query(set_query0[i])
        for i in range(nq1):
            SFSA.query(set1[i])
        for i in range(nq2):
            SFSA.query(set2[i])
        for i in range(nq12):
            SFSA.query(set12[i])
        end = time.time()
        time_consume = end - start
        query_thp_SFSA2.append(N / time_consume)

        ##test of precision
        # test of ShBFA
        correct_number_ShBFA = 0
        for i in range(nq0):
            if ShBFA.query(set_query0[i]) == False:
                correct_number_ShBFA += 1
        for i in range(nq1):
            if ShBFA.query(set1[i]) == 1:
                correct_number_ShBFA += 1
        for i in range(nq2):
            if ShBFA.query(set2[i]) == 2:
                correct_number_ShBFA += 1
        for i in range(nq12):
            if ShBFA.query(set12[i]) == 12:
                correct_number_ShBFA += 1
        precision_ShBFA2.append(correct_number_ShBFA / N)

        # test of SFSA
        correct_number_SFSA = 0
        for i in range(nq0):
            if SFSA.query(set_query0[i]) == 0:
                correct_number_SFSA += 1
        for i in range(nq1):
            if SFSA.query(set1[i]) == 1:
                correct_number_SFSA += 1
        for i in range(nq2):
            if SFSA.query(set2[i]) == 2:
                correct_number_SFSA += 1
        for i in range(nq12):
            if SFSA.query(set12[i]) == 3:
                correct_number_SFSA += 1
        precision_SFSA2.append(correct_number_SFSA / N)

        ##test of delete throughput
        # test of SFSA
        start = time.time()
        for i in range(nq0):
            SFSA.delete(set_query0[i])
        for i in range(nq1):
            SFSA.delete(set1[i])
        for i in range(nq2):
            SFSA.delete(set2[i])
        for i in range(nq12):
            SFSA.delete(set12[i])
        end = time.time()
        time_consume = end - start
        delete_thp_SFSA2.append(N / time_consume)

    insert_thp_ShBFA.append(np.mean(insert_thp_ShBFA2))
    insert_thp_SFSA.append(np.mean(insert_thp_SFSA2))

    query_thp_ShBFA.append(np.mean(query_thp_ShBFA2))
    query_thp_SFSA.append(np.mean(query_thp_SFSA2))

    delete_thp_SFSA.append(np.mean(delete_thp_SFSA2))

    precision_SFSA.append(np.mean(precision_SFSA2))
    precision_ShBFA.append(np.mean(precision_ShBFA2))

print("ShBFA insert thp", insert_thp_ShBFA)
print("SFSA insert thp", insert_thp_SFSA)
print("ShBFA query thp", query_thp_ShBFA)
print("SFSA query thp", query_thp_SFSA)
print("SFSA delete thp", delete_thp_SFSA)
print("ShBFA precision", precision_ShBFA)
print("SFSA precision", precision_SFSA)

RESULT.append("  ")
RESULT.append("insert_thp_ShBFA=" + str(insert_thp_ShBFA))
RESULT.append("insert_thp_SFSA=" + str(insert_thp_SFSA))
RESULT.append(" ")
RESULT.append("query_thp_ShBFA=" + str(query_thp_ShBFA))
RESULT.append("query_thp_SFSA=" + str(query_thp_SFSA))
RESULT.append(" ")
RESULT.append("delete_thp_SFSA=" + str(delete_thp_SFSA))
RESULT.append(" ")
RESULT.append("precision_ShBFA=" + str(precision_ShBFA))
RESULT.append("precision_SFSA=" + str(precision_SFSA))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Association_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("performance_Osore_2sets_2", RESULT)
