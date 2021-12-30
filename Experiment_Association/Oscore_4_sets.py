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

cishu = 20
print("测试次数为：", cishu)
RESULT.append("实验次数：" + str(cishu))

# 存储集合，这里三个集合S1、S2和S3


S = [1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234, 1234]

Rate = [[0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.175, 0.175, 0.175, 0.175, 0.00833, 0.00833, 0.00833, 0.00833, 0.00833, 0.00835, 0.05, 0.05, 0.05, 0.05,
         0.05],
        [0.075, 0.075, 0.075, 0.075, 0.05833, 0.05833, 0.05833, 0.05833, 0.05833, 0.05835, 0.05, 0.05, 0.05, 0.05,
         0.15],
        [0.0625, 0.0625, 0.0625, 0.0625, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.0375, 0.0375, 0.0375, 0.0375,
         0.45],
        [0.025, 0.025, 0.025, 0.025, 0.01666, 0.01666, 0.01666, 0.01666, 0.01666, 0.0167, 0.025, 0.025, 0.025, 0.025,
         0.7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

Rate_query = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0.6, 0.05, 0.05, 0.05, 0.05, 0.00833, 0.00833, 0.00833, 0.00833, 0.00833, 0.00835, 0.025, 0.025, 0.025,
               0.025, 0.05],
              [0.3, 0.0625, 0.0625, 0.0625, 0.0625, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.0375, 0.0375, 0.0375,
               0.0375, 0.15],
              [0.25, 0.0125, 0.0125, 0.0125, 0.0125, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.0375, 0.0375, 0.0375,
               0.0375, 0.4],
              [0.05, 0.025, 0.025, 0.025, 0.025, 0.01666, 0.01666, 0.01666, 0.01666, 0.01666, 0.0167, 0.025, 0.025,
               0.025, 0.025, 0.65],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

O_score = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
RESULT.append("自变量O分数的范围：" + str(O_score))

RESULT.append("ShBFA设计：" + "ShBFA = Shifting_BloomFilter_A(k=12, m=int(2 ** 20 * 20), w=57, sets=S)")
RESULT.append(
    "SFSA设计：" + "SFSA = SFS_A(capacity=2 ** 18, bucket_size=4, markbits=4, fingerprint_size=16,max_displacements=500)")

alpha = 0.95
N = alpha * 2 ** 20

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
        n3 = int(N * Rate[r][2])
        n4 = int(N * Rate[r][3])
        n12 = int(N * Rate[r][4])
        n13 = int(N * Rate[r][5])
        n14 = int(N * Rate[r][6])
        n23 = int(N * Rate[r][7])
        n24 = int(N * Rate[r][8])
        n34 = int(N * Rate[r][9])
        n123 = int(N * Rate[r][10])
        n124 = int(N * Rate[r][11])
        n134 = int(N * Rate[r][12])
        n234 = int(N * Rate[r][13])
        n1234 = int(N * Rate[r][14])

        # two CFs for set1, set2, set3, set4
        CF1 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)
        CF2 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)
        CF3 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)
        CF4 = CuckooFilter(capacity=2 ** 18, bucket_size=4, fingerprint_size=16, max_displacements=500)

        # creat storage datasets
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

        # creat set3
        set3 = [0 for i in range(n3)]
        for num in range(n3):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set3[num] = "".join(sa)
        for i in range(len(set3)):
            CF3.insert(set3[i])

        # creat set4
        set4 = [0 for i in range(n4)]
        for num in range(n4):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set4[num] = "".join(sa)
        for i in range(len(set4)):
            CF4.insert(set4[i])

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

        # creat set13
        set13 = [0 for i in range(n13)]
        for num in range(n13):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set13[num] = "".join(sa)
        for i in range(len(set13)):
            CF1.insert(set13[i])
        for i in range(len(set13)):
            CF3.insert(set13[i])

        # creat set14
        set14 = [0 for i in range(n14)]
        for num in range(n14):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set14[num] = "".join(sa)
        for i in range(len(set14)):
            CF1.insert(set14[i])
        for i in range(len(set14)):
            CF4.insert(set14[i])

        # creat set23
        set23 = [0 for i in range(n23)]
        for num in range(n23):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set23[num] = "".join(sa)
        for i in range(len(set23)):
            CF2.insert(set23[i])
        for i in range(len(set23)):
            CF3.insert(set23[i])

        # creat set24
        set24 = [0 for i in range(n24)]
        for num in range(n24):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set24[num] = "".join(sa)
        for i in range(len(set24)):
            CF2.insert(set24[i])
        for i in range(len(set24)):
            CF4.insert(set24[i])

        # creat set34
        set34 = [0 for i in range(n34)]
        for num in range(n34):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set34[num] = "".join(sa)
        for i in range(len(set34)):
            CF3.insert(set34[i])
        for i in range(len(set34)):
            CF4.insert(set34[i])

        # creat set123
        set123 = [0 for i in range(n123)]
        for num in range(n123):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set123[num] = "".join(sa)
        for i in range(len(set123)):
            CF1.insert(set123[i])
        for i in range(len(set123)):
            CF2.insert(set123[i])
        for i in range(len(set123)):
            CF3.insert(set123[i])

        # creat set124
        set124 = [0 for i in range(n124)]
        for num in range(n124):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set124[num] = "".join(sa)
        for i in range(len(set124)):
            CF1.insert(set124[i])
        for i in range(len(set124)):
            CF2.insert(set124[i])
        for i in range(len(set124)):
            CF4.insert(set124[i])

        # creat set134
        set134 = [0 for i in range(n134)]
        for num in range(n134):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set134[num] = "".join(sa)
        for i in range(len(set134)):
            CF1.insert(set134[i])
        for i in range(len(set134)):
            CF3.insert(set134[i])
        for i in range(len(set134)):
            CF4.insert(set134[i])

        # creat set234
        set234 = [0 for i in range(n234)]
        for num in range(n234):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set234[num] = "".join(sa)
        for i in range(len(set234)):
            CF2.insert(set234[i])
        for i in range(len(set234)):
            CF3.insert(set234[i])
        for i in range(len(set234)):
            CF4.insert(set234[i])

        # creat set1234
        set1234 = [0 for i in range(n1234)]
        for num in range(n1234):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            set1234[num] = "".join(sa)
        for i in range(len(set1234)):
            CF1.insert(set1234[i])
        for i in range(len(set1234)):
            CF2.insert(set1234[i])
        for i in range(len(set1234)):
            CF3.insert(set1234[i])
        for i in range(len(set1234)):
            CF4.insert(set1234[i])

        ShBFA = Shifting_BloomFilter_A(k=12, m=int(2 ** 20 * 20), w=57, sets=S)
        SFSA = SFS_A(capacity=2 ** 18, bucket_size=4, fingerprint_size=16,
                     max_displacements=500)

        ## test of insertion throughput
        # ShBFA存储
        start = time.time()
        for i in range(len(set1)):
            CF1.query(set1[i])
            CF2.query(set1[i])
            CF3.query(set1[i])
            CF4.query(set1[i])
            ShBFA.insert(content=set1[i], mark=[1])
        for i in range(len(set2)):
            CF1.query(set2[i])
            CF2.query(set2[i])
            CF3.query(set2[i])
            CF4.query(set2[i])
            ShBFA.insert(content=set2[i], mark=[2])
        for i in range(len(set3)):
            CF1.query(set3[i])
            CF2.query(set3[i])
            CF3.query(set3[i])
            CF4.query(set3[i])
            ShBFA.insert(content=set3[i], mark=[3])
        for i in range(len(set4)):
            CF1.query(set4[i])
            CF2.query(set4[i])
            CF3.query(set4[i])
            CF4.query(set4[i])
            ShBFA.insert(content=set4[i], mark=[4])
        for i in range(len(set12)):
            CF1.query(set12[i])
            CF2.query(set12[i])
            CF3.query(set12[i])
            CF4.query(set12[i])
            ShBFA.insert(content=set12[i], mark=[12])
        for i in range(len(set13)):
            CF1.query(set13[i])
            CF2.query(set13[i])
            CF3.query(set13[i])
            CF4.query(set13[i])
            ShBFA.insert(content=set13[i], mark=[13])
        for i in range(len(set14)):
            CF1.query(set14[i])
            CF2.query(set14[i])
            CF3.query(set14[i])
            CF4.query(set14[i])
            ShBFA.insert(content=set14[i], mark=[14])
        for i in range(len(set23)):
            CF1.query(set23[i])
            CF2.query(set23[i])
            CF3.query(set23[i])
            CF4.query(set23[i])
            ShBFA.insert(content=set23[i], mark=[23])
        for i in range(len(set24)):
            CF1.query(set24[i])
            CF2.query(set24[i])
            CF3.query(set24[i])
            CF4.query(set24[i])
            ShBFA.insert(content=set24[i], mark=[24])
        for i in range(len(set34)):
            CF1.query(set34[i])
            CF2.query(set34[i])
            CF3.query(set34[i])
            CF4.query(set34[i])
            ShBFA.insert(content=set34[i], mark=[34])
        for i in range(len(set123)):
            CF1.query(set123[i])
            CF2.query(set123[i])
            CF3.query(set123[i])
            CF4.query(set123[i])
            ShBFA.insert(content=set123[i], mark=[123])
        for i in range(len(set124)):
            CF1.query(set124[i])
            CF2.query(set124[i])
            CF3.query(set124[i])
            CF4.query(set124[i])
            ShBFA.insert(content=set124[i], mark=[124])
        for i in range(len(set134)):
            CF1.query(set134[i])
            CF2.query(set134[i])
            CF3.query(set134[i])
            CF4.query(set134[i])
            ShBFA.insert(content=set134[i], mark=[134])
        for i in range(len(set234)):
            CF1.query(set234[i])
            CF2.query(set234[i])
            CF3.query(set234[i])
            CF4.query(set234[i])
            ShBFA.insert(content=set234[i], mark=[234])
        for i in range(len(set1234)):
            CF1.query(set1234[i])
            CF2.query(set1234[i])
            CF3.query(set1234[i])
            CF4.query(set1234[i])
            ShBFA.insert(content=set1234[i], mark=[1234])
        end = time.time()
        time_consume = end - start
        insert_thp_ShBFA2.append(N / time_consume)

        # SFSA存储
        start = time.time()
        for i in range(len(set1)):
            SFSA.insert(item=set1[i], Mark=1)
        for i in range(len(set2)):
            SFSA.insert(item=set2[i], Mark=2)
        for i in range(len(set3)):
            SFSA.insert(item=set3[i], Mark=3)
        for i in range(len(set4)):
            SFSA.insert(item=set4[i], Mark=4)

        for i in range(len(set12)):
            SFSA.insert(item=set12[i], Mark=5)
        for i in range(len(set13)):
            SFSA.insert(item=set13[i], Mark=6)
        for i in range(len(set14)):
            SFSA.insert(item=set14[i], Mark=7)
        for i in range(len(set23)):
            SFSA.insert(item=set23[i], Mark=8)
        for i in range(len(set24)):
            SFSA.insert(item=set24[i], Mark=9)
        for i in range(len(set34)):
            SFSA.insert(item=set34[i], Mark=10)

        for i in range(len(set123)):
            SFSA.insert(item=set123[i], Mark=11)
        for i in range(len(set124)):
            SFSA.insert(item=set124[i], Mark=12)
        for i in range(len(set134)):
            SFSA.insert(item=set134[i], Mark=13)
        for i in range(len(set234)):
            SFSA.insert(item=set234[i], Mark=14)

        for i in range(len(set1234)):
            SFSA.insert(item=set1234[i], Mark=15)

        end = time.time()
        time_consume = end - start
        insert_thp_SFSA2.append(N / time_consume)

        # creat query sets
        nq0 = int(N * Rate_query[r][0])
        nq1 = int(N * Rate_query[r][1])
        nq2 = int(N * Rate_query[r][2])
        nq3 = int(N * Rate_query[r][3])
        nq4 = int(N * Rate_query[r][4])
        nq12 = int(N * Rate_query[r][5])
        nq13 = int(N * Rate_query[r][6])
        nq14 = int(N * Rate_query[r][7])
        nq23 = int(N * Rate_query[r][8])
        nq24 = int(N * Rate_query[r][9])
        nq34 = int(N * Rate_query[r][10])
        nq123 = int(N * Rate_query[r][11])
        nq124 = int(N * Rate_query[r][12])
        nq134 = int(N * Rate_query[r][13])
        nq234 = int(N * Rate_query[r][14])
        nq1234 = int(N * Rate_query[r][15])

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
        for i in range(nq3):
            ShBFA.query(set3[i])
        for i in range(nq4):
            ShBFA.query(set4[i])

        for i in range(nq12):
            ShBFA.query(set12[i])
        for i in range(nq13):
            ShBFA.query(set13[i])
        for i in range(nq14):
            ShBFA.query(set14[i])
        for i in range(nq23):
            ShBFA.query(set23[i])
        for i in range(nq24):
            ShBFA.query(set24[i])
        for i in range(nq34):
            ShBFA.query(set34[i])

        for i in range(nq123):
            ShBFA.query(set123[i])
        for i in range(nq124):
            ShBFA.query(set124[i])
        for i in range(nq134):
            ShBFA.query(set134[i])
        for i in range(nq234):
            ShBFA.query(set234[i])

        for i in range(nq1234):
            ShBFA.query(set1234[i])

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
        for i in range(nq3):
            SFSA.query(set3[i])
        for i in range(nq4):
            SFSA.query(set4[i])

        for i in range(nq12):
            SFSA.query(set12[i])
        for i in range(nq13):
            SFSA.query(set13[i])
        for i in range(nq14):
            SFSA.query(set14[i])
        for i in range(nq23):
            SFSA.query(set23[i])
        for i in range(nq24):
            SFSA.query(set24[i])
        for i in range(nq34):
            SFSA.query(set34[i])

        for i in range(nq123):
            SFSA.query(set123[i])
        for i in range(nq124):
            SFSA.query(set124[i])
        for i in range(nq134):
            SFSA.query(set134[i])
        for i in range(nq234):
            SFSA.query(set234[i])

        for i in range(nq1234):
            SFSA.query(set1234[i])

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
        for i in range(nq3):
            if ShBFA.query(set3[i]) == 3:
                correct_number_ShBFA += 1
        for i in range(nq4):
            if ShBFA.query(set4[i]) == 4:
                correct_number_ShBFA += 1

        for i in range(nq12):
            if ShBFA.query(set12[i]) == 12:
                correct_number_ShBFA += 1
        for i in range(nq13):
            if ShBFA.query(set13[i]) == 13:
                correct_number_ShBFA += 1
        for i in range(nq14):
            if ShBFA.query(set14[i]) == 14:
                correct_number_ShBFA += 1
        for i in range(nq23):
            if ShBFA.query(set23[i]) == 23:
                correct_number_ShBFA += 1
        for i in range(nq24):
            if ShBFA.query(set24[i]) == 24:
                correct_number_ShBFA += 1
        for i in range(nq34):
            if ShBFA.query(set34[i]) == 34:
                correct_number_ShBFA += 1

        for i in range(nq123):
            if ShBFA.query(set123[i]) == 123:
                correct_number_ShBFA += 1
        for i in range(nq124):
            if ShBFA.query(set124[i]) == 124:
                correct_number_ShBFA += 1
        for i in range(nq134):
            if ShBFA.query(set134[i]) == 134:
                correct_number_ShBFA += 1
        for i in range(nq234):
            if ShBFA.query(set234[i]) == 234:
                correct_number_ShBFA += 1

        for i in range(nq1234):
            if ShBFA.query(set1234[i]) == 1234:
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
        for i in range(nq3):
            if SFSA.query(set3[i]) == 3:
                correct_number_SFSA += 1
        for i in range(nq4):
            if SFSA.query(set4[i]) == 4:
                correct_number_SFSA += 1

        for i in range(nq12):
            if SFSA.query(set12[i]) == 5:
                correct_number_SFSA += 1
        for i in range(nq13):
            if SFSA.query(set13[i]) == 6:
                correct_number_SFSA += 1
        for i in range(nq14):
            if SFSA.query(set14[i]) == 7:
                correct_number_SFSA += 1
        for i in range(nq23):
            if SFSA.query(set23[i]) == 8:
                correct_number_SFSA += 1
        for i in range(nq24):
            if SFSA.query(set24[i]) == 9:
                correct_number_SFSA += 1
        for i in range(nq34):
            if SFSA.query(set34[i]) == 10:
                correct_number_SFSA += 1

        for i in range(nq123):
            if SFSA.query(set123[i]) == 11:
                correct_number_SFSA += 1
        for i in range(nq124):
            if SFSA.query(set124[i]) == 12:
                correct_number_SFSA += 1
        for i in range(nq134):
            if SFSA.query(set134[i]) == 13:
                correct_number_SFSA += 1
        for i in range(nq234):
            if SFSA.query(set234[i]) == 14:
                correct_number_SFSA += 1

        for i in range(nq1234):
            if SFSA.query(set1234[i]) == 15:
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
        for i in range(nq3):
            SFSA.delete(set3[i])
        for i in range(nq4):
            SFSA.delete(set4[i])

        for i in range(nq12):
            SFSA.delete(set12[i])
        for i in range(nq13):
            SFSA.delete(set13[i])
        for i in range(nq14):
            SFSA.delete(set14[i])
        for i in range(nq23):
            SFSA.delete(set23[i])
        for i in range(nq24):
            SFSA.delete(set24[i])
        for i in range(nq34):
            SFSA.delete(set34[i])

        for i in range(nq123):
            SFSA.delete(set123[i])
        for i in range(nq124):
            SFSA.delete(set124[i])
        for i in range(nq134):
            SFSA.delete(set134[i])
        for i in range(nq234):
            SFSA.delete(set234[i])

        for i in range(nq1234):
            SFSA.delete(set1234[i])

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
RESULT.append("query_thp_ShBFA=" + str(query_thp_ShBFA))
RESULT.append("query_thp_SFSA=" + str(query_thp_SFSA))
RESULT.append("delete_thp_SFSA=" + str(delete_thp_SFSA))
RESULT.append("precision_ShBFA=" + str(precision_ShBFA))
RESULT.append("precision_SFSA=" + str(precision_SFSA))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Association_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("performance_Osore_4sets", RESULT)
