import os
import numpy as np
import pandas as pd
import scipy.io as io


# # 读取单个文件的时间点数据
def load_patient(subj_path):
    # 读取subj对应的数据
    df = pd.read_csv(subj_path, sep="\t", header=0)
    # 获取ROI序号
    ROIs = ["#" + str(y) for y in sorted([int(x[1:]) for x in df.keys().tolist()])]
    # 读取脑区序号对应的时间序列
    time_course = df[ROIs].values

    # 判断是否存在全零的列
    zero_col = np.zeros(time_course.shape[0])
    for i in range(time_course.shape[1]):
        time_course_col = time_course[0:, i]
        if (time_course_col == zero_col).all():
            # 高亮显示
            print('\033[1;36;40m该文件存在全零列\033[0m', subj_path)
            break
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


def compute_corr(subj_path, time_course, subjs_root, file_id):
    # 打印被试路径方便查找
    print('--------------------------------' + subj_path + '--------------------------------')
    # 计算皮尔逊相关
    corr = np.corrcoef(x=time_course, rowvar=False)
    corr = corr.astype(np.float64)
    # 将皮尔逊相关系数存储为mat格式
    if not os.path.exists(subjs_root.replace('raw', 'FC')):
        os.makedirs(subjs_root.replace('raw', 'FC'))
        io.savemat(subj_path.replace('raw', 'FC').replace('.1D', '.mat'), {file_id + '_fng_FC': corr})
    else:
        io.savemat(subj_path.replace('raw', 'FC').replace('.1D', '.mat'), {file_id + '_fng_FC': corr})

    # 取上三角拉平为一维arry
    arr = upper(corr)
    # 将一维皮尔逊存储为mat格式
    if not os.path.exists(subjs_root.replace('raw', 'arr')):
        os.makedirs(subjs_root.replace('raw', 'arr'))
        io.savemat(subj_path.replace('raw', 'arr').replace('.1D', '.mat'), {file_id + '_fng_arr': arr})
    else:
        io.savemat(subj_path.replace('raw', 'arr').replace('.1D', '.mat'), {file_id + '_fng_arr': arr})

    # 对皮尔逊矩阵进行z变换
    # 防止分母为零报错
    np.fill_diagonal(a=corr, val=0)
    # fisher z
    z_FC = 0.5 * np.log((1 + corr) / (1 - corr))
    z_FC = z_FC.astype(np.float)
    # 对角线还原为1
    np.fill_diagonal(a=corr, val=1.)
    np.fill_diagonal(a=z_FC, val=1.)
    # 将z变换皮尔逊存储为mat格式
    if not os.path.exists(subjs_root.replace('raw', 'z_FC')):
        os.makedirs(subjs_root.replace('raw', 'z_FC'))
        io.savemat(subj_path.replace('raw', 'z_FC').replace('.1D', '.mat'), {file_id + '_fng_z_FC': z_FC})
    else:
        io.savemat(subj_path.replace('raw', 'z_FC').replace('.1D', '.mat'), {file_id + '_fng_z_FC': z_FC})

    z_arr = upper(z_FC)
    # 将一维z变换皮尔逊存储为mat格式
    if not os.path.exists(subjs_root.replace('raw', 'z_arr')):
        os.makedirs(subjs_root.replace('raw', 'z_arr'))
        io.savemat(subj_path.replace('raw', 'z_arr').replace('.1D', '.mat'), {file_id + '_fng_z_arr': z_arr})
    else:
        io.savemat(subj_path.replace('raw', 'z_arr').replace('.1D', '.mat'), {file_id + '_fng_z_arr': z_arr})

if __name__ == '__main__':
    # 分机构计算
    root = 'E:/ABIDE/cpac/raw/filt_noglobal/rois_cc200'
    sites = os.listdir(root)
    # 数据路径
    # site = 'Yale'
    for site in sites:
        # 机构路径
        subjs_root = "E:/ABIDE/cpac/raw/filt_noglobal/rois_cc200/" + site
        # 包含该文件夹下的所有文件名
        files = os.listdir(subjs_root)

        for i in range(len(files)):
            subj_path = subjs_root + '/' + files[i]
            file_id = files[i].replace('.1D', '')
            time_course = load_patient(subj_path)
            compute_corr(time_course=time_course, subj_path=subj_path, subjs_root=subjs_root, file_id=file_id)
        print(
            '********************************* ' + site + ' is over ' + '********************************* ')
