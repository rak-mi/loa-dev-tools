from utils import screenshot

import argparse

parser = argparse.ArgumentParser(description='nah')

parser.add_argument('-type1', metavar='t', type=str,help='Screenshot folder')
parser.add_argument('-type2', metavar='p', type=str, help='Market or Currency description')
parser.add_argument('-mode', metavar='m', type=str, help='Mode (Screenshot description')
parser.add_argument('-W', metavar='m', type=str, help='Width')
parser.add_argument('-H', metavar='m', type=str, help='Height')

args = parser.parse_args()

screenshot.take_screenshot_of_window(args.type1, args.type2, args.mode, args.w, args.h)