from task2 import *
array_mask = [[0,0,0,1,1],[0,1,0,1,0],[1,1,1,1,0],[1,1,1,0,0]]

def testConvertToTiff():
    assert ConvertToTiff('pictures/pic1.jpg') == 'pictures/pic1.tiff'
    assert ConvertToTiff('pictures/x.jpg') == 'No such file or directory'


def testGetSizeOfRaster():
    assert GetSizeOfRaster('pictures/pic1.jpg') == 3840000.0
    assert GetSizeOfRaster('pictures/x.jpg') == 'No such file or directory'


def testGetTheBiggestRaster():
    assert GetTheBiggestRaster('pictures/pic1.jpg', 'pictures/pic2.jpg') == 1

def testIsGray():
    
    assert IsGray([1,1,1]) == True
    assert IsGray([3,1,1]) == False


def testMarkGrayPixels():
    array_mask = [[0,0],[0,0]]
    rgb_array = [[[23,23,23],[1,2,3]],[[3,3,3],[3,3,5]]]
    assert MarkGrayPixels(array_mask, rgb_array) == [[1,0],[1,0]]
    

def testFindTheWay():
    assert FindTheWay(array_mask) == [[2,0],[2,1],[2,2],[2,3]]


def testMarkWay():
    assert MarkWay(array_mask) == [[0,0,0,1,1],[0,1,0,1,0],[2,2,2,2,0],[1,1,1,0,0]]


# def testSetDataToMask():
#     assert SetDataToMask()

# def testClanWay():
#     raster = 'pictures/pic4.tiff'+
#     assert ClanWay()