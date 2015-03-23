
# parses data scraped from HOT tasking manager
# produces a TSV: project area and completion stats

from collections import defaultdict
import glob
import os.path

import processing

datadir = '/home/martin/osm/outputs/20150323-hot-scraper/data'
infilespec = '%s/*/tasks.json' % datadir
outdir = '/home/martin/osm/outputs/20150323-hot-scraper/merged'
outfilename = '%s/project_stats.txt' % outdir

stateFieldName = 'state'
taskStates = {
  0: 'ready',
  1: 'invalidated',
  2: 'done',
  3: 'validated',
  -1: 'removed'
}

outfile = open(outfilename, 'w')
outfile.write('id\tarea\tnum_tasks\t%s\n' % '\t'.join(taskStates.values()))

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  layer = qgis.utils.iface.addVectorLayer(infilename, 'tasks-%s' % id, 'ogr')
  
  total_area = 0
  num_tasks = 0
  task_counter = defaultdict(int)
  statusAttrIdx = layer.fieldNameIndex(stateFieldName)
  
  for inFeat in processing.features(layer):
    total_area += inFeat.geometry().area()
    num_tasks += 1
    task_counter[inFeat.attributes()[statusAttrIdx]] += 1
  
  outfile.write('%s\t%f\t%d' % (id, total_area, num_tasks))
  for key in taskStates.keys():
    outfile.write('\t%d' % task_counter[key])
  outfile.write('\n')
  
  QgsMapLayerRegistry.instance().removeMapLayers([layer.id()])

outfile.close()


