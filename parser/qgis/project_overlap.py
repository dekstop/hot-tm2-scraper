
# parses data scraped from HOT tasking manager
# produces TSV: number and list of overlapping project bounds

layername = 'HOT-projects'
idfieldname = 'id'

outdir = '/home/martin/osm/outputs/20150323-hot-scraper/merged'
mapoutfilename = '%s/project_overlap_map.txt' % (outdir)
countoutfilename = '%s/project_overlap_count.txt' % (outdir)

layers = QgsMapLayerRegistry.instance().mapLayersByName(layername)
if len(layers) != 1:
  print 'Wrong number of layers selected: ', len(layers)

layer = layers[0]
idfieldIdx = layer.fieldNameIndex(idfieldname)

mapoutfile = open(mapoutfilename, 'w')
mapoutfile.write('%s\toverlapping_%s\toverlap_area\n' % (idfieldname, idfieldname))

countoutfile = open(countoutfilename, 'w')
countoutfile.write('%s\tnum_overlaps\ttotal_overlap_area\n' % idfieldname)

for feature1 in layer.getFeatures():
  id1 = feature1.attributes()[idfieldIdx]
  overlaps = []
  overlap_area = 0.0
  for feature2 in layer.getFeatures():
    id2 = feature2.attributes()[idfieldIdx]
    if id1 != id2: # avoid self-comparisons
      if feature1.geometry().intersects(feature2.geometry()):
        intersection = feature1.geometry().intersection(feature2.geometry())
        overlaps.append(id2)
        area = intersection.area()
        overlap_area += area
        mapoutfile.write('%s\t%s\t%f\t%f\t%f\n' % (id1, id2, area, feature1.geometry().area(), feature2.geometry().area()))
  
  countoutfile.write('%s\t%d\t%f\n' % (id1, len(overlaps), overlap_area))

mapoutfile.close()
countoutfile.close()


