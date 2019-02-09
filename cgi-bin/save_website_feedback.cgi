#!/usr/bin/python

import sys
import json
import cgi
import os

form = cgi.FieldStorage()
comment = form.getfirst('comment')

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

result = {}
result['success'] = True

question_file = open('/srv/nlmaps/web_files/website_feedback.txt', 'a')

print >>question_file, "%s" % comment

question_file.close()
sys.stdout.write(json.dumps(result,indent=1))
sys.stdout.write("\n")
sys.stdout.close()