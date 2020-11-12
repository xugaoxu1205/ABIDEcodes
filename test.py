# import os
# sites=os.listdir('E:/ABIDE/cpac/rois/raw/normal/filt_global/rois_cc200')
# print(sites)
# for site in sites:
#     os.makedirs('E:/ABIDE/dparsf/rois/normal/filt_global/rois_cc200/{}'.format(site))
import numpy as np


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
    print(tHOFC)


if __name__ == '__main__':
    time_course = np.random.random((10, 6))
    # print('time_course\n', time_course.shape)
    compute_tHOFC_corr(time_course=time_course)
