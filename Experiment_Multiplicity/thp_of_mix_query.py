#####频数估计的查询实验（查询吞吐量，取正态分布，频数平均值取20）#####
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

##分布的参数设置
normal_loc = 2 ** 5 * 32
normal_scale = 2 ** 5
bits = 16 + 5

RESULT.append("混合查询测试")

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
RESULT.append(
    "SFBX = SFB_X(capacity=2 ** 18, bucket_size=2 ** 2, fingerprint_size=16, block_number=2 ** 5,max_displacements=500)")
RESULT.append("ABF = Adaptive_BloomFilter(k=12,m=math.ceil(capacity * bit),max=max(y))")
RESULT.append("SBF = Shifting_BloomFilter_X(k=12,m=math.ceil(capacity * bit),max=max(y))")

###实验部分

##输出分布的参数配置
print("      ")
print("###分布参数的配置###")
print("正态分布的平均值为：", normal_loc)
print("正态分布的标准差为：", normal_scale)

print("  ")
print("###实验结果--混合查询吞吐量###")

##实现正态分布的随机抽样##
np.random.seed(1)
x1 = np.random.normal(loc=normal_loc, scale=normal_scale, size=capacity)

y1 = []
for i in range(len(x1)):
    z = math.ceil(x1[i])
    if z >= 1:
        y1.append(z)
    else:
        y1.append(1)

y = y1
##开始实验##

SFSX_result = []
SFBX_result = []
ABF_result = []
SBF_result = []

rate_array = np.arange(0.05, 1, 0.05)
print(rate_array)
RESULT.append("fraction of queries on existing items:" + str(rate_array))

for i_r in range(len(rate_array)):
    rate = rate_array[i_r]
    print("fraction of queries on existing items:", rate)

    SFSX_result_temporary = []
    SFBX_result_temporary = []
    ABF_result_temporary = []
    SBF_result_temporary = []

    for times in range(cishu):

        # 测试插入随机字符串
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()+=_-"
        testdata = [0 for i in range(capacity)]
        for num in range(capacity):
            sa = []
            for i in range(16):
                sa.append(random.choice(alphabet))
            testdata[num] = "".join(sa)

        # 测试查询的随机字符串（不存在的）
        testdata1 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(17):
                sa.append(random.choice(alphabet))
            testdata1[num2] = "".join(sa)

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

        # SFSX的实验
        SFSX = SFS_X(capacity=2 ** 15, bucket_size=2 ** 5, fingerprint_size=16,
                     max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            SFSX.insert(testdata[i], y[i])

        start = time.time()
        for i in range(len(testdata2)):
            SFSX.query(testdata2[i])
        end = time.time()
        SFSX_result_temporary.append(len(testdata2) / (end - start))

        # SFBX的实验
        SFBX = SFB_X(capacity=2 ** 18, bucket_size=2 ** 2, fingerprint_size=16, block_number=2 ** 5,
                     max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            SFBX.insert(testdata[i], y[i])

        start = time.time()
        for i in range(len(testdata2)):
            SFBX.query(testdata2[i])
        end = time.time()
        SFBX_result_temporary.append(len(testdata2) / (end - start))

        # ABF使用12个哈希函数的实验
        ABF = Adaptive_BloomFilter(k=12,
                                   m=math.ceil(capacity * bits),
                                   max=max(y))
        for i in range(int(alpha * len(testdata))):
            ABF.insert(testdata[i], y[i])

        start = time.time()
        for i in range(len(testdata2)):
            ABF.query(testdata2[i])
        end = time.time()
        ABF_result_temporary.append(len(testdata2) / (end - start))

        # SBF使用12个哈希函数
        SBF = Shifting_BloomFilter_X(k=12,
                                     m=math.ceil(capacity * bits),
                                     max=max(y))
        for i in range(int(alpha * len(testdata))):
            SBF.insert(testdata[i], y[i])

        start = time.time()
        for i in range(len(testdata2)):
            SBF.query(testdata2[i])
        end = time.time()
        SBF_result_temporary.append(len(testdata2) / (end - start))

    SFSX_result.append(np.mean(SFSX_result_temporary))
    SFBX_result.append(np.mean(SFBX_result_temporary))
    ABF_result.append(np.mean(ABF_result_temporary))
    SBF_result.append(np.mean(SBF_result_temporary))

print("混合查询吞吐量 of SFSX:", SFSX_result)
print("混合查询吞吐量 of SFBX:", SFBX_result)
print("混合查询吞吐量 of ABF:", ABF_result)
print("混合查询吞吐量 of SBF:", SBF_result)

RESULT.append("mix lookup thp")
RESULT.append("SFSX" + "=" + str(SFSX_result))
RESULT.append("SFBX" + "=" + str(SFBX_result))
RESULT.append("ABF" + "=" + str(ABF_result))
RESULT.append("SBF" + "=" + str(SBF_result))


def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Multiplicity_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("X_mix_query_thp", RESULT)
