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
import logging
import sys
from typing import List, Optional, Union

ArgType = Optional[Union[argparse.Namespace, List[str]]]


def setup_log(verbosity: int) -> None:
    """get logger with appropriate logging level and message"""
    if verbosity == 1:
        level = logging.getLevelName("INFO")
    elif verbosity >= 2:
        level = logging.getLevelName("DEBUG")
    else:
        level = logging.getLevelName("WARNING")
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )
    logging.captureWarnings(True)


def arg_parser() -> argparse.ArgumentParser:
    desc = "ROBEX v1.2 T1-w Brain Extraction"
    parser = argparse.ArgumentParser(description=desc)
    required = parser.add_argument_group("Required")
    required.add_argument(
        "t1_image", type=str, help="path to T1-w image to be skull-stripped"
    )
    options = parser.add_argument_group("Options")
    options.add_argument(
        "-os",
        "--output-stripped",
        type=str,
        default=None,
        help="path to output stripped image",
    )
    options.add_argument(
        "-om",
        "--output-mask",
        type=str,
        default=None,
        help="path to output brain mask",
    )
    options.add_argument(
        "-s",
        "--seed",
        type=int,
        default=0,
        help="random seed for reproducible results",
    )
    options.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity (e.g., -vv is more than -v)",
    )
    return parser


def check_args(args: argparse.Namespace) -> None:
    if args.output_stripped is None and args.output_mask is None:
        msg = "--output-stripped and/or --output-mask should be specified,\n"
        msg += "otherwise this script has no output.\nAborting."
        from pyrobex.errors import PyRobexError

        raise PyRobexError(msg)


def main(args: ArgType = None) -> int:
    """Console script for pyrobex."""
    parser = arg_parser()
    if args is None:
        args = parser.parse_args()
    elif isinstance(args, list):
        args = parser.parse_args(args)
    setup_log(args.verbosity)
    logger = logging.getLogger(__name__)
    # import pyrobex here for logging backend
    from pyrobex.io import NiftiImage
    from pyrobex.robex import robex

    check_args(args)
    image = NiftiImage.load(args.t1_image)
    stripped, mask = robex(image, args.seed)
    if args.output_stripped is not None:
        stripped.to_filename(args.output_stripped)
        msg = f"Output skull-stripped image saved to: {args.output_stripped}."
        logger.info(msg)
    if args.output_mask is not None:
        mask.to_filename(args.output_mask)
        msg = f"Output mask image saved to: {args.output_mask}"
        logger.info(msg)
    return 0


if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args()
    sys.exit(main(args))  # pragma: no cover
