# -*- coding: utf-8 -*-
import codecs
import re
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Given a English question and a tagging sequence, where L indicates a location, P a POI and O otherwise, it extracts the corresponding location and POI names from the English question')
    parser.add_argument('--input', '-i', required=True,
                        help='Location of the input en file with original POIs and locations'),
    parser.add_argument('--tagged', '-t', required=True,
                        help='Location for the tagged output sequence file (e.g.  O O L O P)')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def read_lines_in_list(file_to_read):
    list = []
    with open(file_to_read, 'r') as f:
        for line in f:
            list.append(line.rstrip('\n'))
    return list

def write_list_to_file(list, file_to_write):
    with open(file_to_write, 'w') as f:
        for line in list:
            print >>f, line
    return 0

def main():
    parsed_arguments = parse_arguments()
    en_in = read_lines_in_list(parsed_arguments.input)
    tagged_in = read_lines_in_list(parsed_arguments.tagged)
    if len(en_in) != len(tagged_in):
        exit(1)
    pois = []
    locations = []
    for (i, line) in enumerate(tagged_in): 
        pois_line = []
        locations_line = []
        tagged_line = tagged_in[i].split(" ")
        en_line = en_in[i].split(" ")
        collect_poi = ""
        collect_location = ""
        for (j,  word) in enumerate(tagged_line): 
            if word == 'P':
                try:
                    collect_poi += en_line[j]
                    try:
                        if tagged_line[j+1] == 'P':
                            collect_poi += " "
                        else:
                            pois_line.append(collect_poi.strip())
                            collect_poi = ""
                    except IndexError:
                            pois_line.append(collect_poi.strip())
                            collect_poi = ""
                except:
                    pass
            if word == 'L':
                try:
                    collect_location += en_line[j]
                    try:
                        if tagged_line[j+1] == 'L':
                            collect_location += " "
                        else:
                            locations_line.append(collect_location.strip())
                            collect_location = ""
                    except IndexError:
                        locations_line.append(collect_location.strip())
                        collect_location = ""
                except:
                    pass
        pois.append(", ".join(pois_line))
        locations.append(", ".join(locations_line))
                
    write_list_to_file(pois, "%s.pois" % parsed_arguments.tagged)
    write_list_to_file(locations, "%s.locations" % parsed_arguments.tagged)

if __name__ == '__main__':
    main()
