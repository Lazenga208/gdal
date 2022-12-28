import sys
from django.contrib.gis.geos import Point
from osgeo import ogr

ogr.UseExceptions()
driver = ogr.GetDriverByName("ESRI Shapefile")
outName = ("new_file.shp")

# opening the FileGDB
try:
    gdb = ogr.Open("shapeFilesData/AFG_adm2.shp", update = True)
except Exception:
    print("Exeption")
    sys.exit()

# ulx, width, xrot, uly, yrot, height = gdb2.GetGeoTransform()
# lrx = ulx + (ds.RasterXSize * width)
# lry = uly + (ds.RasterYSize * height)
# print(ulx)
for layer in gdb:
    fld = ogr.FieldDefn("distance",ogr.OFTInteger)
    layer.CreateField(fld)
    try:
        output = driver.CreateDataSource(outName)
    except:
        print('Could not create',outName)
    newLayer = output.CreateLayer('new_file',geom_type = ogr.wkbPolygon)
    if newLayer is None:
        print('Could not create layer for buffer in output DS')
        sys.exit(1)
    newLayerDef = newLayer.GetLayerDefn()
    for feature in layer:
        geom = feature.GetGeometryRef()
        ring = geom.GetGeometryRef(0)
        pointCount = ring.GetPointCount()
        points = ring.GetPoints()
        # print(ring.GetPoints())
        # print('--------------------------')
        # for f in points:
            # print(f)
        area = geom.GetArea()
        if feature.GetField("NAME_2") == 'Char Burjak':
            for l in layer:
                geom2 = l.GetGeometryRef()
                ring2 = geom2.GetGeometryRef(0)
                if geom2.GetGeometryName() == "POLYGON":
                    point = Point(ring.GetPoint())
                    point2 = Point(ring2.GetPoint())
                    distance = ring.Distance(ring2)
                    if distance < 1:
                        l.SetField("distance", 1)
                        layer.SetFeature(l)
                    else:
                        l.SetField("distance", 0)
                        layer.SetFeature(l)       
                else:
                    print("geometryName:  ",geom2.GetGeometryName())
        if area > 1:
            print("FID:",feature.GetFID())
            print("area",area)
            print("NAME_2:",feature.GetField("NAME_2"))
            # print("points",points)
            powerBuffer = geom.Buffer(250)
            bufferContains = powerBuffer.Contains(geom)
            if bufferContains == True:
                try:
                    newFeature = ogr.Feature(newLayerDef)
                    newFeature.SetGeometry(geom)
                    newFeature.SetFID(feature.GetFID())
                    newLayer.CreateFeature(newFeature)
                except:
                    print("Error printing shapefile")
                    newFeature.Destroy()
    print('Wrote', 'parcels to shapefile.')

# clean close
del gdb