
# parses data scraped from HOT tasking manager
# produces a shapefile of project boundaries, one feature per project

import glob
import os
import os.path
import sys

from osgeo import ogr
ogr.UseExceptions()

if len(sys.argv) != 4:
    sys.stderr.write('Usage: <datadir> <outdir> <shapefilename>')
    sys.exit(1)

datadir = sys.argv[1]
outdir = sys.argv[2]
shapefilename = sys.argv[3]
if not os.path.isdir(outdir):
    os.makedirs(outdir) 

infilespec = '%s/*/tasks.json' % datadir
outfilename = '%s/%s.shp' % (outdir, shapefilename)
geometryType = ogr.wkbPolygon
driver = ogr.GetDriverByName('ESRI Shapefile')

if os.path.exists(outfilename):
    driver.DeleteDataSource(outfilename)

out_ds = driver.CreateDataSource(outfilename)
out_layer = None

for infilename in glob.glob(infilespec):
    print infilename
    id = os.path.basename(os.path.dirname(infilename))

    # Blacklisted...
    if id in ['738', '1020']:
        # 738: project never launched, and empty geometry crashes QGIS/GDAL
        # 1020: wrong CRS
        print "Skipping this one..."
        continue

    # load input layer
    try:
        dataSource = ogr.Open(infilename)
    except Exception, e:
        print "Failed to load the file:", e
        continue

    # we construct the output layer lazily so we can copy the source CRS.
    if out_layer==None:
        layer = dataSource.GetLayer()
        spatialref = layer.GetSpatialRef()
        out_layer = out_ds.CreateLayer(outfilename, geom_type=geometryType, srs=spatialref)
        idField = ogr.FieldDefn("id", ogr.OFTInteger)
        out_layer.CreateField(idField)
    
    # dissolve all input features into a single feature
    dissolved = dataSource.ExecuteSQL("SELECT ST_Union(geometry) as geometry FROM OGRGeoJSON", None, "SQLITE") 
    
    # and write to output, along with id
    for feature in dissolved: # just one feature
        out_feat = ogr.Feature(out_layer.GetLayerDefn())
        out_feat.SetField('id', id)
        out_feat.SetGeometry(feature.GetGeometryRef().Clone())
        out_layer.CreateFeature(out_feat)
        out_layer.SyncToDisk()

