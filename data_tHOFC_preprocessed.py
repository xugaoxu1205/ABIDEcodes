import os
import numpy as np
import pandas as pd
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


def compute_tHOFC_corr(time_course):
    # 一阶的FC计算
    low_corr = np.corrcoef(x=time_course, rowvar=False)
    low_corr = low_corr.astype(np.float64)
    # print('low_corr\n', low_corr)
    # 获取脑区个数
    nROI = low_corr.shape[0]
    temp_Net = np.zeros(shape=[nROI, nROI])
    for i in range(nROI - 1):
        for j in range((i + 1), nROI):
            # 取两个脑区的皮尔逊相关
            temp1 = low_corr[:, i]
            temp2 = low_corr[:, j]
            # 删除i，j位置的元素，注意：需要有接受副本的变量
            temp1_del = np.delete(arr=temp1, obj=[i, j])
            temp2_del = np.delete(arr=temp2, obj=[i, j])
            thofc = np.corrcoef(temp1_del, temp2_del)
            temp_Net[i, j] = thofc[0][1]
    tHOFC = temp_Net + temp_Net.T
    if not os.path.exists('thofc'):
        os.makedirs('thofc')
        io.savemat('thofc.mat', {'test_tHOFC': tHOFC})
    else:
        io.savemat('thofc.mat', {'test_tHOFC': tHOFC})


if __name__ == '__main__':
    time_course = np.random.random((10, 7))
    print(time_course.shape)
    compute_tHOFC_corr(time_course=time_course)
