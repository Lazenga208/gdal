from osgeo import gdal
import numpy as np


# משימה א
# a
def convertToTiff(raster):
    src = gdal.Open(raster)
    newRaster = raster.split(".")[0]+".tiff"
    gdal.Translate(newRaster, src)
    return newRaster


def getSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
    xres, yres = raster.GetGeoTransform()[1:6:4]
    width = (raster.RasterXSize) * xres
    height = (raster.RasterYSize) * yres
    # print(raster.ReadAsArray())
    # print("RasterCountr:", raster.RasterCount)
    return width * height


def getTheBiggestRaster(raster1, raster2):
    raster1Size = getSizeOfRaster(raster1)
    raster2Size = getSizeOfRaster(raster2)
    if (raster1Size > raster2Size):
        return 1
    else:
        return 2


print(getTheBiggestRaster('pictures/pic1.jpg', 'pictures/pic2.jpg'))
print(getTheBiggestRaster('pictures/pic1.jpg', 'pictures/pic3.jpg'))
print(getTheBiggestRaster('pictures/pic3.jpg', 'pictures/pic2.jpg'))

# b
def IsGray(rgb):
    if all(element == rgb[0] for element in rgb):
        return True
    return False


# path = convertToTiff('pictures/pic4.jpg')

raster = gdal.Open('pictures/pic4.tiff')
band1 = raster.GetRasterBand(1).ReadAsArray()
band2 = raster.GetRasterBand(2).ReadAsArray()
band3 = raster.GetRasterBand(3).ReadAsArray()
rgb_array = np.dstack([band1, band2, band3])
mask = gdal.Open('pictures/pic4.tiff.msk', 1)
array_mask = mask.ReadAsArray()
array_raster = raster.ReadAsArray()


def MarkGrayPixels(array_mask):
    for i in range(len(array_mask)):
        for j in range(len(array_mask[i])):
            if IsGray(rgb_array[i][j]):
                array_mask[i][j] = 1


def FindTheWay(array_mask):
    maxArr = []
    arr = []
    tempArr = []
    for i in range(len(array_mask)):
        for j in range(len(array_mask[i])):
            if (array_mask[i][j] == 1):
                arr.append([i, j])
            else:
                if (arr != []):
                    if (len(arr) > len(tempArr)):
                        tempArr = arr
                    arr = []
        if (len(arr) < len(tempArr)):
            arr = tempArr
        if (len(arr) > len(maxArr)):
            maxArr = arr
        arr = []
    return maxArr


def MarkWay(array_mask):
    way = FindTheWay(array_mask)
    row = way[0][0]
    for i in range(len(way)):
        array_mask[row][way[i][1]] = 2


MarkGrayPixels(array_mask)
MarkWay(array_mask)

mask.GetRasterBand(1).WriteArray(array_mask)
update_mask = mask.ReadAsArray()

