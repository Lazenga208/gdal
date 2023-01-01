# תרגיל 1 GDAL
from osgeo import ogr

path_to_shp_data = "shapeFilesData/AFG_adm2.shp"
dataSource = ogr.Open(path_to_shp_data, update=True)
layer = dataSource.GetLayer(0)
# layer.CreateField(ogr.FieldDefn("Distance", ogr.OFTInteger))
# layer.CreateField(ogr.FieldDefn("Neighbors", ogr.OFTInteger))


def getFid(feature):
    return (feature.GetFID())

def getArea(feature):
    geom = feature.GetGeometryRef()
    return (geom.GetArea())

def GetName_2(feature):
    return (feature.GetField('NAME_2'))

def getPoints(feature):
    geom = feature.GetGeometryRef()
    ring = geom.GetGeometryRef(0)
    return ring.GetPoints()

# א
def printDetails(features):
    for feature in features:
        # א1
        print("FID: ", getFid(feature))
        # א2
        print("Area: ", getArea(feature))
        # א3
        print("NAME_2: ", GetName_2(feature))
        # א4
        print("Vertices: ", getPoints(feature))

features = [feature for feature in layer if (feature.GetGeometryRef().GetArea()) >= 1]
# printDetails(features)

# ב
def getFeatureByName(name='Char Burjak'):
    for feature in layer:
        if feature.GetField('NAME_2') == name:
            return feature


def newField(name, value, feature):
    feature.SetField(name, value)
    layer.SetFeature(feature)
    print(feature.ExportToJson())


def addFieldDistance():
    selectedFeature = getFeatureByName()
    for feature in layer:
        if selectedFeature.GetGeometryRef().Distance(feature.GetGeometryRef()) < 1:
            newField("Distance", 1, feature)
        else:
            newField("Distance", 0, feature)


def addFieldNeighbors():
    features2 = [feature for feature in layer]
    geomes = [geom.GetGeometryRef() for geom in features2]
    for i in range(len(geomes)):
        countNeighbors = 0
        for j in range(len(geomes)):
            if i == j:
                continue
            if geomes[i].Touches(geomes[j]):
                countNeighbors += 1
        newField("Neighbors", countNeighbors, layer[i])

# addFieldDistance()
# addFieldNeighbors()

# ג
def convertToLineString(feature):
    line = ogr.Geometry(ogr.wkbLineString)
    points = getPoints(feature)
    for p in points:
        line.AddPoint(p[0], p[1])
    return line


def newShapeFile():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outName = ("new_file.shp")
    output = driver.CreateDataSource(outName)
    newLayer = output.CreateLayer('new_file', geom_type=ogr.wkbLineString)
    newLayerDef = newLayer.GetLayerDefn()
    for f in features:
        line = convertToLineString(f)
        newFeature = ogr.Feature(newLayerDef)
        newFeature.SetGeometry(line)
        newFeature.SetFID(getFid(f))
        newLayer.CreateFeature(newFeature)


def readShapeFile():
    dataSource2 = ogr.Open('new_file.shp')
    layer2 = dataSource2.GetLayer(0)
    for f in layer2:
        print(f.ExportToJson())

# newShapeFile()
# readShapeFile()

# ד
def MaxArea():
    maxArea = 0
    for f in features:
        area = getArea(f)
        if area > maxArea:
            maxArea = area
            maxFeature = f
    return maxFeature


def MaxNeighbors():
    maxNeighbors = 0
    for f in layer:
        if f.GetField('Neighbors') > maxNeighbors:
            maxNeighbors = f.GetField('Neighbors')
            maxfeature = f
    return maxfeature


def newPoint(pointsArea, maxNeighbors, i, j):
    point1 = ogr.Geometry(ogr.wkbPoint)
    point2 = ogr.Geometry(ogr.wkbPoint)
    point1.AddPoint(pointsArea.GetX(i), pointsArea.GetY(i))
    point2.AddPoint(maxNeighbors.GetX(j), maxNeighbors.GetY(j))
    return point1, point2


def getTwopoints():
    maxArea = MaxArea()
    maxNeighbors = MaxNeighbors()
    pointsArea = maxArea.GetGeometryRef().GetGeometryRef(0)
    pointsNeighbors = maxNeighbors.GetGeometryRef().GetGeometryRef(0)
    point1, point2 = newPoint(pointsArea, pointsNeighbors, 0, 0)
    minDistance = point1.Distance(point2)
    minPoint1 = point1
    minPoint2 = point2

    for i in range(pointsArea.GetPointCount()):
        for j in range(pointsNeighbors.GetPointCount()):
            point1, point2 = newPoint(pointsArea, pointsNeighbors, i, j)
            distance = point1.Distance(point2)
            if minDistance > distance:
                minDistance = distance
                minPoint1 = point1
                minPoint2 = point2
    addLineString(minPoint1, minPoint2)


def addLineString(point1, point2):
    dataSource2 = ogr.Open('new_file.shp', update = True)
    layer2 = dataSource2.GetLayer(0)
    newLayerDef = layer2.GetLayerDefn()
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(point1.GetX(), point1.GetY())
    line.AddPoint(point2.GetX(), point2.GetY())
    newFeature = ogr.Feature(newLayerDef)
    newFeature.SetGeometry(line)
    layer2.CreateFeature(newFeature)
    print(line)


getTwopoints()
readShapeFile()
