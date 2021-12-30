#####频数估计的查询实验（查询准确度和假阳性以及相对误差）#####
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
cishu = 3

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

SFSX_zqd = []
SFBX_zqd = []
ABF_zqd = []
SBF_zqd = []

SFSX_fp = []
SFBX_fp = []
ABF_fp = []
SBF_fp = []

SFSX_are = []
SFBX_are = []
ABF_are = []
SBF_are = []

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

    ##开始实验##

    SFSX_zqd2 = []
    SFBX_zqd2 = []
    ABF_zqd2 = []
    SBF_zqd2 = []

    SFSX_fp2 = []
    SFBX_fp2 = []
    ABF_fp2 = []
    SBF_fp2 = []

    SFSX_are2 = []
    SFBX_are2 = []
    ABF_are2 = []
    SBF_are2 = []

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
        testdata2 = [0 for i in range(capacity)]
        for num2 in range(capacity):
            sa = []
            for i in range(17):
                sa.append(random.choice(alphabet))
            testdata2[num2] = "".join(sa)

        # SFSX的实验
        SFSX = SFS_X(capacity=2 ** 15, bucket_size=2 ** 5, fingerprint_size=16,
                     max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            SFSX.insert(testdata[i], y[i])
        # 准确度实验
        count_zqd = 0
        count_false = 0
        for i in range(int(alpha * len(testdata))):
            zqd = SFSX.query(testdata[i])
            if zqd == False:
                count_false += 1

            if zqd != y[i] and zqd != False:
                count_zqd += 1
        SFSX_zqd2.append(1 - (count_zqd / (int(alpha * len(testdata) - count_false))))
        # 假阳性实验
        count_fp = 0
        for i in range(int(alpha * len(testdata2))):
            fp = SFSX.query(testdata2[i])
            if fp != False:
                count_fp += 1
        SFSX_fp2.append(count_fp / int(alpha * len(testdata2)))
        # 平均相对误差实验
        count_are = 0
        c_f = 0
        for i in range(int(alpha * len(testdata))):
            are = SFSX.query(testdata[i])
            if are != False:
                c_f += y[i]
                count_are += abs(are - y[i])
        SFSX_are2.append(count_are / c_f)

        # SFBX的实验
        SFBX = SFB_X(capacity=2 ** 18, bucket_size=2 ** 2, fingerprint_size=16, block_number=2 ** 5,
                     max_displacements=500)
        for i in range(int(alpha * len(testdata))):
            SFBX.insert(testdata[i], y[i])
        # 准确度实验
        count_zqd = 0
        count_false = 0
        for i in range(int(alpha * len(testdata))):
            zqd = SFBX.query(testdata[i])
            if zqd == False:
                count_false += 1
            if zqd != y[i] and zqd != False:
                count_zqd += 1
        SFBX_zqd2.append(1 - (count_zqd / (int(alpha * len(testdata) - count_false))))
        # 假阳性实验
        count_fp = 0
        for i in range(int(alpha * len(testdata2))):
            fp = SFBX.query(testdata2[i])
            if fp != False:
                count_fp += 1
        SFBX_fp2.append(count_fp / int(alpha * len(testdata2)))
        # 平均相对误差实验
        count_are = 0
        c_f = 0
        for i in range(int(alpha * len(testdata))):
            are = SFBX.query(testdata[i])
            if are != False:
                c_f += y[i]
                count_are += abs(are - y[i])
        SFBX_are2.append(count_are / c_f)

        # ABF使用12个哈希函数的实验
        ABF = Adaptive_BloomFilter(k=12,
                                   m=math.ceil(capacity * bit),
                                   max=max(y))
        for i in range(int(alpha * len(testdata))):
            ABF.insert(testdata[i], y[i])
        # 准确度实验
        count_zqd = 0
        for i in range(int(alpha * len(testdata))):
            zqd = ABF.query(testdata[i])
            if zqd != y[i]:
                count_zqd += 1
        ABF_zqd2.append(1 - (count_zqd / int(alpha * len(testdata))))
        # 假阳性实验
        count_fp = 0
        for i in range(int(alpha * len(testdata2))):
            fp = ABF.query(testdata2[i])
            if fp != False:
                count_fp += 1
        ABF_fp2.append(count_fp / int(alpha * len(testdata2)))
        # 平均相对误差实验
        count_are = 0
        sum_y = 0
        for i in range(int(alpha * len(testdata))):
            are = ABF.query(testdata[i])
            if are != False:
                count_are += abs(are - y[i])  # TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'
                sum_y += y[i]
        ABF_are2.append(count_are / sum_y)

        # SBF使用12个哈希函数
        SBF = Shifting_BloomFilter_X(k=12,
                                     m=math.ceil(capacity * bit),
                                     max=max(y))
        for i in range(int(alpha * len(testdata))):
            SBF.insert(testdata[i], y[i])
        # 准确度实验
        count_zqd = 0
        for i in range(int(alpha * len(testdata))):
            zqd = SBF.query(testdata[i])
            if zqd != y[i]:
                count_zqd += 1
        SBF_zqd2.append(1 - (count_zqd / int(alpha * len(testdata))))
        # 假阳性实验
        count_fp = 0
        for i in range(int(alpha * len(testdata2))):
            fp = SBF.query(testdata2[i])
            if fp != 0:
                count_fp += 1
        SBF_fp2.append(count_fp / int(alpha * len(testdata2)))
        # 平均相对误差实验
        count_are = 0
        sum_y = 0
        for i in range(int(alpha * len(testdata))):
            are = SBF.query(testdata[i])
            count_are += abs(are - y[i])
            sum_y += y[i]
        SBF_are2.append(count_are / sum_y)

    SFSX_zqd.append(np.mean(SFSX_zqd2))
    SFBX_zqd.append(np.mean(SFBX_zqd2))
    ABF_zqd.append(np.mean(ABF_zqd2))
    SBF_zqd.append(np.mean(SBF_zqd2))

    SFSX_fp.append(np.mean(SFSX_fp2))
    SFBX_fp.append(np.mean(SFBX_fp2))
    ABF_fp.append(np.mean(ABF_fp2))
    SBF_fp.append(np.mean(SBF_fp2))

    SFSX_are.append(np.mean(SFSX_are2))
    SFBX_are.append(np.mean(SFBX_are2))
    ABF_are.append(np.mean(ABF_are2))
    SBF_are.append(np.mean(SBF_are2))

print("准确度")
print("SFSX:", SFSX_zqd)
print("SFBX:", SFBX_zqd)
print("ABF:", ABF_zqd)
print("SBF:", SBF_zqd)

print("  ")
print("假阳性")
print("SFSX:", SFSX_fp)
print("SFBX:", SFBX_fp)
print("ABF:", ABF_fp)
print("SBF:", SBF_fp)

print(" ")
print("平均相对误差")
print("SFSX:", SFSX_are)
print("SFBX:", SFBX_are)
print("ABF:", ABF_are)
print("SBF:", SBF_are)

RESULT.append("准确度")
RESULT.append("SFSX" + "=" + str(SFSX_zqd))
RESULT.append("SFBX" + "=" + str(SFBX_zqd))
RESULT.append("ABF" + "=" + str(ABF_zqd))
RESULT.append("SBF" + "=" + str(SBF_zqd))

RESULT.append("   ")
RESULT.append("假阳性")
RESULT.append("SFSX" + "=" + str(SFSX_fp))
RESULT.append("SFBX" + "=" + str(SFBX_fp))
RESULT.append("ABF" + "=" + str(ABF_fp))
RESULT.append("SBF" + "=" + str(SBF_fp))

RESULT.append("   ")
RESULT.append("平均相对误差")
RESULT.append("SFSX" + "=" + str(SFSX_are))
RESULT.append("SFBX" + "=" + str(SFBX_are))
RESULT.append("ABF" + "=" + str(ABF_are))
RESULT.append("SBF" + "=" + str(SBF_are))



def text_create(name, msg):
    desktop_path = "F:/Shifting_Filter/Experiment/Multiplicity_Query/"  # 新创建的txt文件的存放路径

    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档

    file = open(full_path, 'w')
    for element in msg:
        file.write(element + "\n")

    file.close()


text_create("X_zqd_fp_ARE", RESULT)
