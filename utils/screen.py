import screenshot

import argparse

parser = argparse.ArgumentParser(description='nah')

parser.add_argument('-t', metavar='type1', type=str,help='Screenshot folder')
parser.add_argument('-p', metavar='type2', type=str, help='Market or Currency description')
parser.add_argument('-m', metavar='mode', type=str, help='Mode (Screenshot description')
parser.add_argument('-W', metavar='w', type=str, help='Width')
parser.add_argument('-H', metavar='h', type=str, help='Height')

args = parser.parse_args()

screenshot.take_screenshot_of_window(args.t, args.p, args.m, args.W, args.H)