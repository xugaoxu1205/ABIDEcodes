import os
sites=os.listdir('E:/ABIDE/cpac/rois/raw/normal/filt_global/rois_cc200')
print(sites)
for site in sites:
    os.makedirs('E:/ABIDE/dparsf/rois/normal/filt_global/rois_cc200/{}'.format(site))