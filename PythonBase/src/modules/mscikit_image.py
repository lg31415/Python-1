#-*-coding:utf-8-*-
import numpy as np
import matplotlib.pyplot as mpl
import scipy.ndimage as ndimage 
import skimage.filter as skif

# Generating data points with a non-uniform background
x = np.random.uniform(low=0, high=100, size=20).astype(int) 
y = np.random.uniform(low=0, high=100, size=20).astype(int)

# Creating image with non-uniform background 
func = lambda x, y: x**2 + y**2
grid_x, grid_y = np.mgrid[-1:1:100j, -2:2:100j] 
bkg = func(grid_x, grid_y)
bkg = bkg / np.max(bkg)

# Creating points
clean = np.zeros((100,100))
clean[(x,y)] += 5
clean = ndimage.gaussian_filter(clean, 3) 
clean = clean / np.max(clean)

# Combining both the non-uniform background and points
fimg = bkg + clean
fimg = fimg / np.max(fimg)

#显示图像
#fig0 = mpl.figure(figsize=(8, 4))
mpl.imshow(fimg)
mpl.plot()


# Defining minimum neighboring size of objects 
block_size = 3

# Adaptive threshold function which returns image
# map of structures that are different relative to background
adaptive_cut = skif.threshold_adaptive(fimg, block_size, offset=0)

# Global threshold
global_thresh = skif.threshold_otsu(fimg) 
global_cut = fimg > global_thresh

# Creating figure to highlight difference between adaptive and global threshold methods
fig = mpl.figure(figsize=(8, 4))
fig.subplots_adjust(hspace=0.05, wspace=0.05)

ax1 = fig.add_subplot(131) 
ax1.imshow(fimg)            #原始图像
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)

ax2 = fig.add_subplot(132) 
ax2.imshow(global_cut)      #全局阈值得到的分割
ax2.xaxis.set_visible(False) 
ax2.yaxis.set_visible(False)

ax3 = fig.add_subplot(133) 
ax3.imshow(adaptive_cut)    #自适应阈值得到的分割
ax3.xaxis.set_visible(False) 
ax3.yaxis.set_visible(False)

fig.savefig('scikit_image_f01.pdf', bbox_inches='tight')

