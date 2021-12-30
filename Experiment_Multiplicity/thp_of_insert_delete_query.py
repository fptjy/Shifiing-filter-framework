#####频数估计的存储实验#####
import sys
import numpy as np
import math
import random
import time

sys.path.append(r"F:/Shifting_Filter/ShBF_ABF")
from ShBF_X import Shifting_BloomFilter_X
from AdaptiveBF import Adaptive_BloomFilter

sys.path.append(r"F:/Shifting_Filter/Shifting_Filter_on_bucket/SF_on_bucket_Multiplicity")
from SFB_Multiplicity import SFB_X

sys.path.append(r"F:/Shifting_Filter/Shifting_Filter_on_slot/SVCF_Multiplicity")
from SFS_Multiplicity import SFS_X

RESULT = []

# 实验参数设置
cishu = 1

alpha = 0.95
size = 2 ** 18
capacity = size * 4

normal_loc = [2 ** 0 * 32, 2 ** 1 * 32, 2 ** 2 * 32, 2 ** 3 * 32, 2 ** 4 * 32, 2 ** 5 * 32]
normal_scale = [2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5]
bits = [16, 16 + 1, 16 + 2, 16 + 3, 16 + 4, 16 + 5]

RESULT.append("存储、查询、删除吞吐量测试")

RESULT.append("###参数配置###")
RESULT.append("实验次数：" + str(cishu))
RESULT.append("空间利用率：" + str(alpha))
RESULT.append("数据结构容量:" + str(capacity))
RESULT.append("正态分布的平均值为：" + str(normal_loc))
RESULT.append("正态分布的标准差为：" + str(normal_scale))
RESULT.append("平均每元素所占比特：" + str(bits))
RESULT.append("  ")

RESULT.append("数据结构设计")
RESULT.append("SFSX = SFS_X(capacity=2 ** 15, bucket_size=2 ** 5, fingerprint_size=16,max_displacements=500)")
RESULT.append("SFBX = SFB_X(capacity=2 ** 18, bucket_size=2 ** 2, fingerprint_size=16, block_number=2 ** 5,max_displacements=500)")
RESULT.append("ABF = Adaptive_BloomFilter(k=12,m=math.ceil(capacity * bit),max=max(y))")
RESULT.append("SBF = Shifting_BloomFilter_X(k=12,m=math.ceil(capacity * bit),max=max(y))")

SFSX_final_result_insert = []
SFBX_final_result_insert = []
ABF_final_result_insert = []
SBF_final_result_insert = []

SFSX_final_result_query_exist = []
SFBX_final_result_query_exist = []
ABF_final_result_query_exist = []
SBF_final_result_query_exist = []

SFSX_final_result_query_alien = []
SFBX_final_result_query_alien = []
ABF_final_result_query_alien = []
SBF_final_result_query_alien = []

SFSX_final_result_delete = []
SFBX_final_result_delete = []

###实验部分
for canshu in range(len(normal_loc)):

    bit = bits[canshu]

    ##实现正态分布的随机抽样##
    np.random.seed(1)
    x1 = np.random.normal(loc=normal_loc[canshu], scale=normal_scale[canshu], size=capacity)

    y1 = []
    for i in range(len(x1)):
        z = math.ceil(x1[i])
        if z >= 1:
            y1.append(z)
        else:
            y1.append(1)

    y = y1

    SFSX_insert = []
    SFBX_insert = []
    ABF_insert = []
    SBF_insert = []

    SFSX_query_exist = []
    SFBX_query_exist = []
    ABF_query_exist = []
    SBF_query_exist = []

    SFSX_query_alien = []
    SFBX_query_alien = []
    ABF_query_alien = []
    SBF_query_alien = []

    SFSX_delete = []
    SFBX_delete = []

    for times in range(cishu):

        # 测试插入和100%存在查询的随机字符串构成的数据集
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 测试100%不存在查询的随机字符串构成的数据集
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata1 = [0 for i in range(capacity)]
        for num1 in range(capacity):
            sa = []
            for i in range(17):
                sa.append(random.choice(alphabet))
            testdata1[num1] = "".join(sa)

        ## SFS的实验
        # 存储实验
        SFSX = SFS_X(capacity=2 ** 15, bucket_size=2 ** 5, fingerprint_size=16,
                     max_displacements=500)
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFSX.insert(testdata[i], y[i])
        end = time.time()
        SFSX_insert.append(int(alpha * len(testdata)) / (end - start))
        # 100%存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFSX.query(testdata[i])
        end = time.time()
        SFSX_query_exist.append(int(alpha * len(testdata)) / (end - start))
        # 100%不存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            SFSX.query(testdata1[i])
        end = time.time()
        SFSX_query_alien.append(int(alpha * len(testdata1)) / (end - start))
        # 删除实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFSX.delete(testdata[i])
        end = time.time()
        SFSX_delete.append(int(alpha * len(testdata)) / (end - start))

        ## SFB的实验
        # 存储实验
        SFBX = SFB_X(capacity=2 ** 18, bucket_size=2 ** 2, fingerprint_size=16, block_number=2 ** 5,
                     max_displacements=500)
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFBX.insert(testdata[i], y[i])
        end = time.time()
        SFBX_insert.append(int(alpha * len(testdata)) / (end - start))
        # 100%存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFBX.query(testdata[i])
        end = time.time()
        SFBX_query_exist.append(int(alpha * len(testdata)) / (end - start))
        # 100%不存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            SFBX.query(testdata1[i])
        end = time.time()
        SFBX_query_alien.append(int(alpha * len(testdata1)) / (end - start))
        # 删除实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SFBX.delete(testdata[i])
        end = time.time()
        SFBX_delete.append(int(alpha * len(testdata)) / (end - start))

        ## ABF使用12个哈希函数的实验
        # 存储实验
        ABF = Adaptive_BloomFilter(k=12,
                                   m=math.ceil(capacity * bit),
                                   max=max(y))
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            ABF.insert(testdata[i], y[i])
        end = time.time()
        # print("ABF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        ABF_insert.append(int(alpha * len(testdata)) / (end - start))
        # 100%存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            ABF.query(testdata[i])
        end = time.time()
        ABF_query_exist.append(int(alpha * len(testdata)) / (end - start))
        # 100%不存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            ABF.query(testdata1[i])
        end = time.time()
        ABF_query_alien.append(int(alpha * len(testdata1)) / (end - start))

        # SBF使用12个哈希函数
        # 存储
        SBF = Shifting_BloomFilter_X(k=12,
                                     m=math.ceil(capacity * bit),
                                     max=max(y))
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SBF.insert(testdata[i], y[i])
        end = time.time()
        # print("SBF4: {:5.3f} seconds to add to capacity, {:10.2f} entries/second".format(
        #     end - start, int(alpha*len(testdata)) / (end - start)))
        SBF_insert.append(int(alpha * len(testdata)) / (end - start))
        # 100%存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata))):
            SBF.query(testdata[i])
        end = time.time()
        SBF_query_exist.append(int(alpha * len(testdata)) / (end - start))
        # 100%不存在查询实验
        start = time.time()
        for i in range(int(alpha * len(testdata1))):
            SBF.query(testdata1[i])
        end = time.time()
        SBF_query_alien.append(int(alpha * len(testdata1)) / (end - start))

    SFSX_final_result_insert.append(np.mean(SFSX_insert))
    SFBX_final_result_insert.append(np.mean(SFBX_insert))
    ABF_final_result_insert.append(np.mean(ABF_insert))
    SBF_final_result_insert.append(np.mean(SBF_insert))

    SFSX_final_result_query_exist.append(np.mean(SFSX_query_exist))
    SFBX_final_result_query_exist.append(np.mean(SFBX_query_exist))
    ABF_final_result_query_exist.append(np.mean(ABF_query_exist))
    SBF_final_result_query_exist.append(np.mean(SBF_query_exist))

    SFSX_final_result_query_alien.append(np.mean(SFSX_query_alien))
    SFBX_final_result_query_alien.append(np.mean(SFBX_query_alien))
    ABF_final_result_query_alien.append(np.mean(ABF_query_alien))
    SBF_final_result_query_alien.append(np.mean(SBF_query_alien))

    SFSX_final_result_delete.append(np.mean(SFSX_delete))
    SFBX_final_result_delete.append(np.mean(SFBX_delete))

print("Insertion thp")
print("SFSX:", SFSX_final_result_insert)
print("SFBX:", SFBX_final_result_insert)
print("ABF:", ABF_final_result_insert)
print("SBF:", SBF_final_result_insert)
print(" ")

print("Lookup thp of 100% exist item")
print("SFSX:", SFSX_final_result_query_exist)
print("SFBX:", SFBX_final_result_query_exist)
print("ABF:", ABF_final_result_query_exist)
print("SBF:", SBF_final_result_query_exist)
print(" ")

print("Lookup thp of 100% alien item")
print("SFSX:", SFSX_final_result_query_alien)
print("SFBX:", SFBX_final_result_query_alien)
print("ABF:", ABF_final_result_query_alien)
print("SBF:", SBF_final_result_query_alien)
print(" ")

print("delete")
print("SFSX", SFSX_final_result_delete)
print("SFBX", SFBX_final_result_delete)

RESULT.append("Insertion thp")
RESULT.append("SFSX" + "=" + str(SFSX_final_result_insert))
RESULT.append("SFBX" + "=" + str(SFBX_final_result_insert))
RESULT.append("ABF" + "=" + str(ABF_final_result_insert))
RESULT.append("SBF" + "=" + str(SBF_final_result_insert))

RESULT.append("Lookup thp of 100% exist item")
RESULT.append("SFSX" + "=" + str(SFSX_final_result_query_exist))
RESULT.append("SFBX" + "=" + str(SFBX_final_result_query_exist))
RESULT.append("ABF" + "=" + str(ABF_final_result_query_exist))
RESULT.append("SBF" + "=" + str(SBF_final_result_query_exist))

RESULT.append("Lookup thp of 100% alien item")
RESULT.append("SFSX" + "=" + str(SFSX_final_result_query_alien))
RESULT.append("SFBX" + "=" + str(SFBX_final_result_query_alien))
RESULT.append("ABF" + "=" + str(ABF_final_result_query_alien))
RESULT.append("SBF" + "=" + str(SBF_final_result_query_alien))

RESULT.append("Delete performance")
RESULT.append("SFSX" + "=" + str(SFSX_final_result_delete))
RESULT.append("SFBX" + "=" + str(SFBX_final_result_delete))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Multiplicity_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("X_thp_insert_query_delete", RESULT)
