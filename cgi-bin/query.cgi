#!/usr/bin/python

import sys
import json
import cgi
import tempfile, shutil
import os
import subprocess
import urllib2
import httplib
import requests 
httplib.HTTPConnection.debuglevel = 1
form = cgi.FieldStorage()
question = form.getfirst('a_question') # will be accessible in $_POST['data1']

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

result = {}
result['success'] = True

question_file = open('/srv/nlmaps/web_files/nlmaps_questions.txt', 'a')

question_only_file = open('/srv/nlmaps/web_files/only_questions.txt', 'a')
print >>question_only_file, "%s" % question
question_only_file.close()


debug_file = open('/srv/nlmaps/web_files/debug.log', 'w')
print >>debug_file, "question: %s" % question

temp_dir = tempfile.mkdtemp(prefix='nlmaps_website_query')

print >>debug_file, "temp_dir 0: %s" % temp_dir
print >>debug_file, "temp_dir exists?: %s" % os.path.isdir(temp_dir)

result['question'] = question

reference_text = form.getfirst('ref_point')
user_lat = form.getfirst('user_lat')
user_lon = form.getfirst('user_lon')
parser_to_use = form.getfirst('parser_to_use')
nominatim_question = ""
ref = "in text"
print >>debug_file, "parser_to_use: %s" % parser_to_use

if reference_text or user_lat:    
    area_ref = 0
    original_reference = "current_gps"
    if user_lat:
        link = "http://open.mapquestapi.com/nominatim/v1/reverse.php?key=API_KEY&format=json&lat=%s&lon=%s&zoom=8" % (user_lat, user_lon)
        nominatim_response = urllib2.urlopen(link).read()
        nominatim_response = json.loads(nominatim_response)
        if nominatim_response["osm_type"] == "way":
            area_ref = int(nominatim_response["osm_id"]) + 2400000000
        if nominatim_response["osm_type"] == "relation":
            area_ref = int(nominatim_response["osm_id"]) + 3600000000
        print >>debug_file, "area_ref: %s" % area_ref
        nominatim_question = "user gps: %s, %s" % (user_lat, user_lon)
        ref = "%s, %s" % (user_lat, user_lon)

    if reference_text:
        original_reference = reference_text
        reference_text = urllib2.quote(reference_text)
        nominatim_response = urllib2.urlopen("https://open.mapquestapi.com/nominatim/v1/search.php?key=API_KEY&format=json&q=%s" % reference_text).read()
        nominatim_response = json.loads(nominatim_response)
        for ele in nominatim_response:
            if ele["osm_type"] == "way":
                area_ref = int(ele["osm_id"]) + 2400000000
                break
            if ele["osm_type"] == "relation":
                area_ref = int(ele["osm_id"]) + 3600000000
                break 
        print >>debug_file, "area_ref: %s" % area_ref
        nominatim_question = "reference text: %s" % reference_text
        ref = reference_text

    print >>debug_file, "question: %s" % question
    question += " in Heidelberg" # fake a location that we know because the parser has been trained to expect a location, Heidelberg is later replaced with the actual user location
    print >>debug_file, "question: %s" % question
        
    question_tmp_file = open('%s/question' % temp_dir, 'w')
    print >>question_tmp_file, question
    question_tmp_file.close()

    question_tmp_file = open('%s/this_reference' % temp_dir, 'w')
    print >>question_tmp_file, "<nom>%s</nom>" % area_ref
    question_tmp_file.close()

    question_tmp_file = open('%s/this_reference_original' % temp_dir, 'w')
    print >>question_tmp_file, "%s" % original_reference
    question_tmp_file.close()
        
    if parser_to_use == 'default':
        args = ["/bin/bash", "/srv/nlmaps/nematus/run_parsing_pipeline_sep_area.sh", temp_dir]
        nullfile = open(os.devnull, 'w')
        log = open('%s/log.err' % temp_dir, 'w')
        p = subprocess.Popen(args, stdin=nullfile, stdout=nullfile, stderr=log)
        p.wait()
        log.close()
        nullfile.close()
    else:
        print >>debug_file, "non-default parser"
  
else:    
    question_tmp_file = open('%s/question' % temp_dir, 'w')
    print >>question_tmp_file, question
    question_tmp_file.close()
    
    if parser_to_use == 'default':
        args = ["/bin/bash", "/srv/nlmaps/nematus/run_parsing_pipeline.sh", temp_dir]
        nullfile = open(os.devnull, 'w')
        log = open('/srv/nlmaps/web_files/log.err', 'w')
        p = subprocess.Popen(args, stdin=nullfile, stdout=log, stderr=log)
        p.wait()
        log.close()
        nullfile.close()
    else:
        print >>debug_file, "non-default parser, question: %s" % question

        # get mrl from external parser
        data = {'question':question}
        question_quoted = urllib2.quote(question)
        url_to_send = "%s?question=%s" % (parser_to_use, question_quoted)
        print >>debug_file, url_to_send
        mrl = urllib2.urlopen(url_to_send).read()
        print >>debug_file, "urllib : %s" % mrl
        
        mrl_tmp_file = open('%s/mrls' % temp_dir, 'w')
        print >>mrl_tmp_file, mrl
        mrl_tmp_file.close()
        args = ["/bin/bash", "/srv/nlmaps/handle_query_db.sh", temp_dir]
        nullfile = open(os.devnull, 'w')
        log = open('/srv/nlmaps/web_files/log.err', 'w')
        p = subprocess.Popen(args, stdin=nullfile, stdout=log, stderr=log)
        p.wait()
        log.close()
        nullfile.close()

question_only_ref_file = open('/srv/nlmaps/web_files/only_questions_ref.txt', 'a')
print >>question_only_ref_file, "%s ||| %s" % (question, ref)
question_only_ref_file.close()

answer = ''
with open('%s/answers' % temp_dir) as answer_file:
  for line in answer_file:
    answer = line.strip().split(", ")
print >>debug_file, "r.answer : %s" % answer


mrl = ''
with open('%s/mrls' % temp_dir) as mrl_file:
  for line in mrl_file:
    mrl = line.strip()

result['sorry'] = True


latlong = ''
with open('%s/latlong' % temp_dir) as latlong_file:
    for line in latlong_file:
        latlong = line.strip()

if latlong != '':
  result['latlong'] = json.loads(latlong)
  result['sorry'] = False

shutil.rmtree(temp_dir)

result['mrl'] = mrl

result['answer'] = answer
print >>question_file, "%s ||| %s ||| %s ||| %s" % (question, nominatim_question, mrl, answer)

print >>debug_file, "temp_dir: %s" % temp_dir
debug_file.close()

question_file.close()
sys.stdout.write(json.dumps(result,indent=1))
sys.stdout.write("\n")
sys.stdout.close()
