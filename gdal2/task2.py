from osgeo import gdal
import numpy as np

# משימה א
# a
def ConvertToTiff(raster):
    src = gdal.Open(raster)
    if src is None:
        return 'No such file or directory'
    newRaster = raster.split(".")[0]+".tiff"
    gdal.Translate(newRaster, src)
    if gdal.Open(newRaster) is not None:
        return newRaster
    else:
        return 'Failed to translate'


def GetSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
    if raster is None:
        return 'No such file or directory'
    xres, yres = raster.GetGeoTransform()[1:6:4]
    width = (raster.RasterXSize) * xres
    height = (raster.RasterYSize) * yres
    return width * height


def GetTheBiggestRaster(raster1, raster2):
    raster1Size = GetSizeOfRaster(raster1)
    raster2Size = GetSizeOfRaster(raster2)
    if (raster1Size > raster2Size):
        return 1
    else:
        return 2


print(GetTheBiggestRaster('pictures/pic1.jpg', 'pictures/pic2.jpg'))
print(GetTheBiggestRaster('pictures/pic1.jpg', 'pictures/pic3.jpg'))
print(GetTheBiggestRaster('pictures/pic3.jpg', 'pictures/pic2.jpg'))


# b
def CropRaster(raster, point1, point2):
    upper_left_x, upper_left_y = point1
    lower_right_x, lower_right_y = point2
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    gdal.Translate("crop"+raster, raster, projWin = window)


CropRaster('pictures/img1.tif', (696278.000, 3668042.000), ( 700374.000, 3665994.000))
CropRaster("pictures/img2.tif",(700373.500, 3663946.500), (704469.500, 3661898.500))
g = gdal.Warp("pictures/output.jpg", ["pictures/img1.jpg","pictures/img2.jpg"])

g = None

# options_list = [
#     '-ot Byte',
#     '-of JPEG',
#     '-b 1',
#     '-scale'
# ]

# options_string = " ".join(options_list)

# gdal.Translate(
#     'pictures/img1.jpg',
#     'pictures/img1.tif',
#     options = options_string
# )
# gdal.Translate(
#     'pictures/img2.jpg',
#     'pictures/img2.tif',
#     options = options_string
# )


# משימה ב
def IsGray(rgb):
    if all(element == rgb[0] for element in rgb):
        return True
    return False


def MarkGrayPixels(array_mask, rgb_array):
    for i in range(len(array_mask)):
        for j in range(len(array_mask[i])):
            if IsGray(rgb_array[i][j]):
                array_mask[i][j] = 1
    return array_mask


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
    return array_mask


def SetDataToMask(raster, mask):
    dsMask = gdal.Open(mask)
    array_mask = dsMask.ReadAsArray()
    dsRaster = gdal.Open(raster)
    band1 = dsRaster.GetRasterBand(1).ReadAsArray()
    band2 = dsRaster.GetRasterBand(2).ReadAsArray()
    band3 = dsRaster.GetRasterBand(3).ReadAsArray()
    rgb_array = np.dstack([band1, band2, band3])
    MarkGrayPixels(array_mask, rgb_array)
    array_mask = MarkWay(array_mask)
    return array_mask


def ClanWay(raster):
    # raster = ConvertToTiff('pictures/pic4.jpg')
    dsRaster = gdal.Open(raster, 1)
    if dsRaster is None:
        return 'No such file or directory'
    dsRaster.CreateMaskBand(gdal.GMF_NODATA)
    mask = gdal.Open(raster+'.msk', 1)
    if mask is None:
        return 'No such file or directory'
    array_mask = SetDataToMask(raster, raster+'.msk')
    mask.GetRasterBand(1).WriteArray(array_mask)


ClanWay('pictures/pic4.tiff')
