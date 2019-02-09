#!/usr/bin/python

import sys
import json
import cgi
import os

form = cgi.FieldStorage()
answer = form.getfirst('answer')
feedback = form.getfirst('helpful') # will be accessible in $_POST['data1']
question = form.getfirst('question')
mrl = form.getfirst('mrl')

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

result = {}
result['success'] = True

question_file = open('/srv/nlmaps/web_files/feedback.txt', 'a')

print >>question_file, "%s ||| %s ||| %s ||| %s" % (question, mrl, answer, feedback)

question_file.close()
sys.stdout.write(json.dumps(result,indent=1))
sys.stdout.write("\n")
sys.stdout.close()