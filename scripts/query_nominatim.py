# -*- coding: utf-8 -*-
import codecs
import re
import argparse
import urllib2
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Given a location, queries Nominatim for the best OSM ID')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), required=True, metavar='PATH', help='Location of input file')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), required=True, metavar='PATH', help='Location of output file')
    parsed_arguments = parser.parse_args()
    return parsed_arguments
    
if __name__ == "__main__":
    parsed_arguments = parse_arguments()
    line = parsed_arguments.input.readlines()
    individual = line[0].strip().split(", ") #assumes file only had 1 line
    noms = ""
    for reference_text in individual:
        if reference_text == "": # then tagger did not identify a location
            break
        reference_text = urllib2.quote(reference_text)
        nominatim_response = urllib2.urlopen("http://open.mapquestapi.com/nominatim/v1/search.php?key=API_KEY&format=json&q=%s" % reference_text).read()
        nominatim_response = json.loads(nominatim_response)
        for ele in nominatim_response:
            if ele["osm_type"] == "way":
                area_ref = int(ele["osm_id"]) + 2400000000
                break
            if ele["osm_type"] == "relation":
                area_ref = int(ele["osm_id"]) + 3600000000
                break
        if noms == "":
            noms += "<nom>%s</nom>" % area_ref
        else:
            noms += ", " + "<nom>%s</nom>" % area_ref
    parsed_arguments.output.write(noms+"\n")