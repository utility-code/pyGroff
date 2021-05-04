import pygroff as pg
from pygroff import compiler
import argparse as ap

arg = ap.ArgumentParser()
arg.add_argument(
    "-l",
    type=str,
    help="Default language string if not python",
    required=False,
    default="python -c",
)
arg.add_argument("-f", type=str, help="Input file path", required=True)
arg.add_argument("-o", type=str, help="Output file path", required=True)
arg.add_argument(
    "-toc", type=str, help="Add table of contents", required=False, default=True
)
arg.add_argument("-c", help="Add cover page", action="store_true")
arg.add_argument(
    "-w", type=bool, help="Convert to word?", required=False, default=False
)
arg.add_argument("-n", type=str, help="Name for cover page", required=False)
arg.add_argument("-t", type=str, help="Title for cover page", required=False)
arg.add_argument(
    "-e",
    type=bool,
    help="Execute python code and return output",
    required=False,
    default=True,
)
arg.add_argument("-i", type=bool, help="Are there images", required=False, default=True)
arg.add_argument(
    "-df", type=str, help="Different date format", required=False, default="%B %d ,%Y"
)
arg.add_argument(
    "-d", type=str, help="Delete intermediates", required=False, default=True
)
ag = arg.parse_args()

compiler.main(ag)
