from osgeo import gdal
#משימה א

#a

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
    raster1 = convertToTiff(raster1)
    raster2 = convertToTiff(raster2)
    raster1Size = getSizeOfRaster(raster1)
    raster2Size = getSizeOfRaster(raster2)
    if(raster1Size > raster2Size):
        return 1
    else:
        return 2
print(getTheBiggestRaster('pictures/1.jpg', 'pictures/2.jpg'))
print(getTheBiggestRaster('pictures/1.jpg', 'pictures/3.jpg'))
print(getTheBiggestRaster('pictures/3.jpg', 'pictures/2.jpg'))

#b
