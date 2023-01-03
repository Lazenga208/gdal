from osgeo import gdal as GD  
import matplotlib.pyplot as mplot  
import numpy as npy  
data_set = GD.Open(r'pictures/1.tiff')  
print(data_set.RasterCount)  
# As, there are 3 bands, we will store in 3 different variables  
band_1 = data_set.GetRasterBand(1) # red channel  
band_2 = data_set.GetRasterBand(2) # green channel  
band_3 = data_set.GetRasterBand(3) # blue channel  
b1 = band_1.ReadAsArray()
b2 = band_2.ReadAsArray()
b3 = band_3.ReadAsArray()
img_1 = npy.dstack((b1, b2, b3))
f = mplot.figure()
mplot.imshow(img_1)
mplot.savefig('Tiff.png')
mplot.show()
