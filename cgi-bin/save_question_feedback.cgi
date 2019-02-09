#!/usr/bin/python

import sys
import json
import cgi
import os

form = cgi.FieldStorage()

question = form.getfirst('repeat_question')
area_radio = form.getfirst('area_feedback')
spelling_radio = form.getfirst('spelling_feedback')
qtype_radio = form.getfirst('qtype_feedback')
osm_tag_radio = form.getfirst('osm_tag_feedback')
overpass_radio = form.getfirst('overpass_feedback')
mrl_radio = form.getfirst('mrl_feedback')

area = form.getfirst('area_feedback_text')
spelling = form.getfirst('spelling_feedback_text')
qtype = form.getfirst('qtype_feedback_text')
osm_tag = form.getfirst('osm_tag_feedback_text')
overpass = form.getfirst('overpass_feedback_text')
mrl = form.getfirst('mrl_feedback_text')

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

result = {}
result['success'] = True

question_file = open('/srv/nlmaps/web_files/question_feedback.txt', 'a')

print >>question_file, "%s ||| %s::::%s ||| %s::::%s ||| %s::::%s ||| %s::::%s ||| %s::::%s ||| %s::::%s" % (question, area_radio, area, spelling_radio, spelling, qtype_radio, qtype, osm_tag_radio, osm_tag, overpass_radio, overpass, mrl_radio, mrl)

question_file.close()
sys.stdout.write(json.dumps(result,indent=1))
sys.stdout.write("\n")
sys.stdout.close()