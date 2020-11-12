import os
import numpy as np
import pandas as pd
import math
import scipy.io as io


# 读取单个文件的时间点数据
def load_patient(subj_path):
    # 读取subj对应的数据
    df = pd.read_csv(subj_path, sep="\t", header=0)
    # 获取ROI序号
    ROIs = ["#" + str(y) for y in sorted([int(x[1:]) for x in df.keys().tolist()])]
    # 读取脑区序号对应的时间序列
    time_course = df[ROIs].values

    return time_course


# 将方阵上三角拉平为一维向量
def upper(matrix):
    matrix = np.array(matrix)
    # 矩阵的长度
    n = matrix.shape[0]
    up = []
    k = -1
    matrix = matrix.reshape([-1, 1])
    for i in range(n):
        for j in range(n):
            k = k + 1
            if i >= j:
                up.append(k)
    arr = np.delete(arr=matrix, obj=up)
    return arr


def compute_dynamic_corr(time_course, w=3, s=1):
    # 时间点个数
    nTime = time_course.shape[0]
    # 滑动窗口的个数
    k = math.floor((nTime - w) / s + 1)
    for i in range(k):
        # 时间窗的开始位置,时间窗的宽度应为w
        start = i * s
        end = i * s + w
        # 计算皮尔逊相关
        corr = np.corrcoef(x=time_course[start: end, :], rowvar=False)
        corr = corr.astype(np.float64)
        if not os.path.exists('test_dFC'):
            os.makedirs('test_dFC')
            io.savemat('./test_dFC/test{}.mat'.format(i), {'test{}'.format(i): corr})
        else:
            io.savemat('./test_dFC/test{}.mat'.format(i), {'test{}'.format(i): corr})


if __name__ == '__main__':
    time_course = np.random.random((10, 3))
    print(time_course.shape)
    compute_dynamic_corr(time_course=time_course)
