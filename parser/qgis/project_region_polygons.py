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
datadir = '/home/martin/osm/outputs/20150323-hot-scraper/data'
outdir = '/home/martin/osm/outputs/20150323-hot-scraper/shapefiles'

infilespec = '%s/*/tasks.json' % datadir
tempfilename = '%s/temp_dissolved.shp' % outdir
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
  
  QgsGeometryAnalyzer().dissolve(layer, tempfilename, onlySelectedFeatures=False, uniqueIdField=-1, p=None)
  QgsMapLayerRegistry.instance().removeMapLayers([layer.id()])
  layer = qgis.utils.iface.addVectorLayer(tempfilename, 'tasks-%s-diss' % id, 'ogr')
  
  try:
    for feature in processing.features(layer):
      outGeom = QgsGeometry(feature.geometry())
      outFeat = QgsFeature(fields)
      outFeat.setGeometry(outGeom)
      outFeat.setAttributes([id])
      writer.addFeature(outFeat)
      if writer.hasError() != QgsVectorFileWriter.NoError:
        print 'Error when creating shapefile: ', writer.hasError()
  except Exception as e:
    print e
  
  QgsMapLayerRegistry.instance().removeMapLayers([layer.id()])

del writer

canvas.freeze(False)
canvas.refresh()

outlayer = qgis.utils.iface.addVectorLayer(outfilename, outlayername, 'ogr')

