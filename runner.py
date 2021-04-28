import pygroff as pg
from pygroff import compiler
import argparse as ap

arg = ap.ArgumentParser()
arg.add_argument("-f", type=str, help="Input file path", required=True)
arg.add_argument("-o", type=str, help="Output file path", required=True)
arg.add_argument("-c", type=bool, help="Add cover page", required=False, default=True)
arg.add_argument("-n", type=str, help="Name for cover page", required=False)
arg.add_argument("-t", type=str, help="Title for cover page", required=False)
arg.add_argument(
    "-df", type=str, help="Different date format", required=False, default="%B %d ,%Y"
)
arg.add_argument(
    "-d", type=str, help="Delete intermediates", required=False, default=True
)
ag = arg.parse_args()

compiler.main(ag)
