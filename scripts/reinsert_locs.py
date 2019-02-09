# -*- coding: utf-8 -*-
import codecs
import re
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Given a MRL with _LOCATION and _POI placeholders, reinsert the original location and POI names.')
    parser.add_argument('--input', '-i', required=True,
                        help='Location of the input mrl file with _LOCATION and _POI'),
    parser.add_argument('--output', '-o', required=True,
                        help='Location for the output file')
    parser.add_argument('--loc', '-l', required=True,
                        help='Location of the loc file')
    parser.add_argument('--poi', '-p', required=True,
                        help='Location of the poi file')
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
    mrl_in = read_lines_in_list(parsed_arguments.input)
    loc_in = read_lines_in_list(parsed_arguments.loc)
    poi_in = read_lines_in_list(parsed_arguments.poi)
    if len(loc_in) != len(mrl_in) or len(poi_in) != len(mrl_in):
        exit(1)
    for (i, line) in enumerate(loc_in):
       for ele in loc_in[i].split(", "):
          mrl_in[i] = mrl_in[i].replace("_LOCATION", ele, 1)
    for (i, line) in enumerate(poi_in):
       split_pois = poi_in[i].split(", ")
       if len(split_pois) == 1:
          mrl_in[i] = mrl_in[i].replace("_POI", line, 1)   
       elif len(split_pois) > 1:
          for ele in split_pois:
             mrl_in[i] = mrl_in[i].replace("_POI", ele, 1)    
    
    write_list_to_file(mrl_in, parsed_arguments.output)

if __name__ == '__main__':
    main()
