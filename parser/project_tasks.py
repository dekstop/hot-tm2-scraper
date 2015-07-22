
# parses data scraped from HOT tasking manager
# produces a TSV: project task count

import glob
import json
import os
import os.path
import sys

if len(sys.argv) != 3:
    sys.stderr.write('Usage: <datadir> <outdir>')
    sys.exit(1)

datadir = sys.argv[1]
outdir = sys.argv[2]
if not os.path.isdir(outdir):
    os.makedirs(outdir)

infilespec = '%s/*/tasks.json' % datadir
outfilename = '%s/project_tasks.txt' % (outdir)

outfile = open(outfilename, 'w')
outfile.write('id\tnum_tasks\n')

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))

  try:
    json_data = open(infilename).read()
    data = json.loads(json_data)
    features = data['features']
    if len(features)>0:
      num_features = len(features)
      outfile.write('%s\t%d\n' % (id, num_features))
  except ValueError:
      pass
outfile.close()


