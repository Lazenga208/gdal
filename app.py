# משימה 1
from osgeo import ogr

path_to_shp_data = "shapeFilesData/AFG_adm2.shp"
dataSource = ogr.Open(path_to_shp_data, update = True)
layer = dataSource.GetLayer(0)
# layer.CreateField(ogr.FieldDefn("Distance", ogr.OFTInteger))
# layer.CreateField(ogr.FieldDefn("Neighbors", ogr.OFTInteger))

def GetFid(feature):
    return(feature.GetFID())

def GetArea(feature):
    geom = feature.GetGeometryRef()
    return(geom.GetArea())

def GetName_2(feature):
    return(feature.GetField('NAME_2'))

def GetPoints(feature):
    geom = feature.GetGeometryRef()
    ring = geom.GetGeometryRef(0)
    return ring.GetPoints()

def GetFeatureByName(name = 'Char Burjak'):
    for feature in layer:
        if feature.GetField('NAME_2') == name:
            return feature

# א
def printDetails(features):
    for feature in features:
        # א1
        print("FID: ", GetFid(feature))
        # א2
        print("Area: ", GetArea(feature))
        # א3
        print("NAME_2: ", GetName_2(feature))
        # א4
        print("Vertices: ", GetPoints(feature))

features = [feature for feature in layer if (feature.GetGeometryRef().GetArea()) >= 1]
# printDetails(features)

# ב
def AddFieldDistance():
    selectedFeature = GetFeatureByName()
    for feature in layer:
        if selectedFeature.GetGeometryRef().Distance(feature.GetGeometryRef()) < 1:
            feature.SetField("Distance", 1)
        else:
            feature.SetField("Distance", 0)
        layer.SetFeature(feature)

def AddFieldNeighbors(feature):
    countNeighbors = 0
    for f in layer:
        if feature.GetGeometryRef().Touches(f.GetGeometryRef()):
            countNeighbors += 1
    feature.SetField("Neighbors", countNeighbors)
    layer.SetFeature(feature)

def AddNewField():
    # AddFieldDistance()
    for feature in layer:
        AddFieldNeighbors(feature)
        print("feature",feature.ExportToJson())

AddNewField()
# ג


