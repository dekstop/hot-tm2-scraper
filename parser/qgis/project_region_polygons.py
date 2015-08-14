# parses data scraped from HOT tasking manager
# produces a QGIS layer and shapefile: all project boundaries

import glob
import os.path

from qgis.analysis import QgsGeometryAnalyzer
import processing

import PyQt4.QtCore
# from PyQt4.QtGui import QFileDialog

# dialog = QFileDialog()
# dialog.setFileMode(QFileDialog.Directory)

# datadir = dialog.getOpenFileName(None, "Input directory with */tasks.json GeoJSON files")
# outdir = dialog.getOpenFileName(None, "Output directory for shapefile")
datadir = '/Users/mongo/osm/data/etl/hotosm_history_20150813/hotosm-tm2/data'
outdir = '/Users/mongo/osm/data/etl/hotosm_history_20150813/hotosm-tm2/shapefiles'

if not os.path.exists(outdir):
  os.makedirs(outdir)

infilespec = '%s/*/tasks.json' % datadir
diss_shapefilename = '%s/temp_dissolved.shp' % outdir
outlayername = 'hot_project_regions'
outfilename = '%s/%s.shp' % (outdir, outlayername)

fields = QgsFields()
fields.append(QgsField('id', PyQt4.QtCore.QVariant.Int, 'Integer'))

canvas = qgis.utils.iface.mapCanvas()
canvas.freeze(True)

writer = None
for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  if id=='738' or id=='1020': 
    # 738: project never launched, and shapefile crashes QGIS
    # 1020: wrong CRS
    print "Skipping this one..."
    continue

  layer = qgis.utils.iface.addVectorLayer(infilename, 'tasks-%s' % id, 'ogr')
  if layer==None:
    print "Failed to load the layer! Check its file format."
    continue
  
  if writer==None:
    # lazy initialisation: we adopt the existing geom type and CRS
    provider = layer.dataProvider()
    QgsVectorFileWriter.deleteShapeFile(outfilename) # clean previous runs
    writer = QgsVectorFileWriter(outfilename, None, fields,
      provider.geometryType(), layer.crs())
 
  QgsGeometryAnalyzer().dissolve(layer, diss_shapefilename, onlySelectedFeatures=False, uniqueIdField=-1, p=None)
  QgsMapLayerRegistry.instance().removeMapLayers([layer.id()])
  diss_layer = qgis.utils.iface.addVectorLayer(diss_shapefilename, 'tasks-%s-diss' % id, 'ogr')
  
  try:
    for feature in processing.features(diss_layer):
      outGeom = QgsGeometry(feature.geometry())
      outFeat = QgsFeature(fields)
      outFeat.setGeometry(outGeom)
      outFeat.setAttributes([id])
      writer.addFeature(outFeat)
      if writer.hasError() != QgsVectorFileWriter.NoError:
        print 'Error when creating shapefile: ', writer.hasError()
  except Exception as e:
    print e
  
  QgsMapLayerRegistry.instance().removeMapLayers([diss_layer.id()])
  QgsVectorFileWriter.deleteShapeFile(diss_shapefilename)

del writer

canvas.freeze(False)
canvas.refresh()

outlayer = qgis.utils.iface.addVectorLayer(outfilename, outlayername, 'ogr')

