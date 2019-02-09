# -*- coding: utf-8 -*-
import re
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_arguments():
    parser = argparse.ArgumentParser(description='A neural network based semantic parser for NLmaps')
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), required=True, metavar='PATH', 
                        help='Location of the input en file with original POIs and locations'),
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), required=True, metavar='PATH', 
                        help='Location for the output file which is now lowercased and tokenised')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    parsed_arguments = parse_arguments()
    en_in = parsed_arguments.input.readlines()
    for (i, line) in enumerate(en_in):
        line = line.lower()
        line = re.sub(r"\?", " ?", line)
        line = re.sub(r"!", " !", line)
        line = re.sub(r",", " ,", line)
        line = re.sub(r";", " ;", line)
        line = re.sub(r"\.$", " .", line)
        parsed_arguments.output.write(line)
                
if __name__ == '__main__':
    main()
