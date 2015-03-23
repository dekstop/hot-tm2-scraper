
# parses data scraped from HOT tasking manager
# produces a TSV: number of contributors

from decimal import Decimal
import glob
import json
import os.path

# Gini coefficient
# From http://planspace.org/2013/06/21/how-to-calculate-gini-coefficient-from-raw-data-in-python/

# values: a list of positive integers
def gini(values):
  sorted_list = sorted(values)
  height, area = 0, 0
  for value in sorted_list:
    height += value
    area += height - value / Decimal(2)
  fair_area = height * len(values) / Decimal(2)
  return (fair_area - area) / fair_area

datadir = '/home/martin/osm/outputs/20150323-hot-scraper/data'
infilespec = '%s/*/contributors.json' % datadir
outdir = '/home/martin/osm/outputs/20150323-hot-scraper/merged'
outfilename = '%s/task_contributors.txt' % (outdir)

outfile = open(outfilename, 'w')
outfile.write('id\tnum_users\tgini\n')

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  
  json_data = open(infilename).read()
  data = json.loads(json_data)
  
  user_task_stats = {
    user: sum([len(v) for v in user_map.values()]) 
    for (user, user_map) in data.iteritems()
  }
  
  num_users = len(data)
  task_gini = 1
  if num_users>0:
    task_gini = gini(user_task_stats.values())
  
  outfile.write('%s\t%d\t%F\n' % (id, num_users, task_gini))

outfile.close()

