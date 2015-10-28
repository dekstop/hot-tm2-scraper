
# parses data scraped from HOT tasking manager
# produces a TSV of project participants

import codecs
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

infilespec = '%s/*/contributors.json' % datadir
outfilename = '%s/project_contributors.txt' % (outdir)

outfile = codecs.open(outfilename, 'w', 'utf-8')
outfile.write('project_id\tusername\tnum_tasks\n')

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  
  json_data = open(infilename).read()
  data = json.loads(json_data)
  
  user_task_stats = {
    user: sum([len(v) for v in user_map.values()]) 
    for (user, user_map) in data.iteritems()
  }
  
  # print user_task_stats
  
  for user in user_task_stats.keys():
    outfile.write('%s\t%s\t%d\n' % (id, user, user_task_stats[user]))

outfile.close()

