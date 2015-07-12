
# parses data scraped from HOT tasking manager
# produces a TSV: project activity period

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

infilespec = '%s/*/stats.json' % datadir
outfilename = '%s/project_activity.txt' % (outdir)

outfile = open(outfilename, 'w')
outfile.write('id\tfirst_date\tlast_date\tdone\tvalidated\n')

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  
  json_data = open(infilename).read()
  data = json.loads(json_data)
  stats = data['stats']
  if len(stats)>0:
    first_record = data['stats'][0]
    last_record = data['stats'][-1]
    
    first_date = first_record[0]
    last_date = last_record[0]
    
    total = data['total']
    last_done = last_record[1]
    last_validated = last_record[2]
    
    rel_done = (last_done + last_validated) / total
    rel_validated = last_validated / total
    
    outfile.write('%s\t%s\t%s\t%F\t%F\n' % (id, first_date, last_date, rel_done, rel_validated))

outfile.close()


