
# parses data scraped from HOT tasking manager
# produces a TSV of project titles

import glob
import os
import os.path
import re
import sys

if len(sys.argv) != 3:
    sys.stderr.write('Usage: <datadir> <outdir>')
    sys.exit(1)

datadir = sys.argv[1]
outdir = sys.argv[2]
if not os.path.isdir(outdir):
    os.makedirs(outdir) 

infilespec = '%s/*/index.html' % datadir
outfilename = '%s/project_description.txt' % (outdir)

title_rexp = re.compile('.*<h1>\s*(?:#\d+ - )?(.*?)\s*(?:\(Archived\)|\(Draft\))*\s*</h1>.*', re.DOTALL)
private_rexp = re.compile('.*403 Forbidden.*', re.DOTALL)
archived_rexp = re.compile('.*\(Archived\).*', re.DOTALL)
draft_rexp = re.compile('.*\(Draft\).*', re.DOTALL)
changeset_rexp = re.compile('.*Changeset Comment\s*<span.*</span>\s*</dt>\s*<dd>\s*(.*?)\s*</dd>.*', re.DOTALL)
newline_rexp = re.compile('[\n\r]', re.DOTALL)

outfile = open(outfilename, 'w')
outfile.write('id\ttitle\tis_private\tis_archived\tis_draft\tchangeset_comment\n')

for infilename in glob.glob(infilespec):
  print infilename
  
  id = os.path.basename(os.path.dirname(infilename))
  
  if id!='627': # for some reason, title matching for this one doesn't terminate
    html = open(infilename).read()
    print "title"
    match = title_rexp.search(html)
    if match:
      title = match.group(1)
      print "newline"
      title = newline_rexp.sub(' ', title)
    
      changeset_comment = ''
      print "changeset"
      changeset_match = changeset_rexp.search(html)
      if changeset_match:
        print "newline"
        changeset_comment = newline_rexp.sub(' ', changeset_match.group(1))
    
      print "flags, write"
      outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (id, title,
        'true' if private_rexp.match(title) else 'false',
        'true' if archived_rexp.match(title) else 'false',
        'true' if draft_rexp.match(title) else 'false',
        changeset_comment
      ))
    else:
      print "Didn't find a title for this document!"

outfile.close()

