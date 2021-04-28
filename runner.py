#!/usr/bin/python
import pygroff as pg
from pygroff import compiler
import argparse as ap

arg = ap.ArgumentParser()
arg.add_argument("-f", type=str, help="Input file path", required=True)
arg.add_argument("-o", type=str, help="Output file path", required=True)
ag = arg.parse_args()

compiler.main(ag)
