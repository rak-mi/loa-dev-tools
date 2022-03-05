from screen_scrape import auto_utils

import argparse

parser = argparse.ArgumentParser(description='nah')

parser.add_argument('x', metavar='t', type=str,
                    help='nah')

parser.add_argument('y', metavar='p', type=str, 
                    help='nah')


args = parser.parse_args()

auto_utils.move_mouse(args.x, args.y)