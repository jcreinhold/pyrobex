#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyrobex.cli

console script for pyrobex

this is a silly script because it provides a python script
interface to a bash script, but it's slightly easier to
deploy because of setup.py and it allows easy testing of
the pyrobex package

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 6, 2021
"""

import argparse
import sys

from pyrobex.io import load
from pyrobex.pyrobex import robex


def arg_parser():
    desc = "ROBEX v1.2 T1-w Brain Extraction"
    parser = argparse.ArgumentParser(description=desc)
    required = parser.add_argument_group('Required')
    required.add_argument('t1_image', type=str,
                          help='path to T1-w image to be skull-stripped')
    options = parser.add_argument_group('Options')
    options.add_argument('-os', '--output-stripped', type=str, default=None,
                         help='path to output stripped image')
    options.add_argument('-om', '--output-mask', type=str, default=None,
                         help='path to output brain mask')
    options.add_argument('-s', '--seed', type=int, default=0,
                         help='random seed for reproducible results')
    return parser


def main(args=None):
    """Console script for pyrobex."""
    if args is None:
        parser = arg_parser()
        args = parser.parse_args()
    image = load(args.t1_image)
    stripped, mask = robex(image, args.seed)
    if args.output_stripped is not None:
        stripped.to_filename(args.output_stripped)
    if args.output_mask is not None:
        mask.to_filename(args.output_mask)
    return 0


if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args()
    sys.exit(main(args))  # pragma: no cover
