from screen_scrape import screenshot

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('type1', metavar='t', type=str,
                    help='an integer for the accumulator')

parser.add_argument('type2', metavar='p', type=str, 
                    help='an integer for the accumulator')

parser.add_argument('mode', metavar='m', type=str, 
                    help='an integer for the accumulator')

args = parser.parse_args()

screenshot.take_screenshot_of_window(args.type1, args.type2, args.mode)