
# parses data scraped from HOT tasking manager
# produces a TSV of project participants

import codecs
import glob
import json
import os.path

datadir = '/home/martin/osm/outputs/20150323-hot-scraper/data'
infilespec = '%s/*/contributors.json' % datadir
outdir = '/home/martin/osm/outputs/20150323-hot-scraper/profiles'
outfilename = '%s/task_contributor_map.txt' % (outdir)

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

