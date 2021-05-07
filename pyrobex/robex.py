# -*- coding: utf-8 -*-
"""
pyrobex.pyrobex

main python wrapper functions for robex

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 5, 2021
"""

__all__ = [
    'robex',
    'robex_mask',
    'robex_stripped',
]

import logging
from pathlib import Path
import subprocess
import tempfile

from pyrobex.errors import PyRobexError
from pyrobex.io import NiftiImage, NiftiImagePair

logger = logging.getLogger(__name__)


def _find_robex_dist() -> str:
    file_path = Path(__file__).resolve()
    pyrobex_dir = file_path.parent
    robex_dist = pyrobex_dir / "ROBEX"
    return str(robex_dist)


def _find_robex_script() -> str:
    robex_dist = Path(_find_robex_dist())
    robex_script = robex_dist / "runROBEX.sh"
    if not robex_script.is_file():
        raise PyRobexError("Could not find `runROBEX.sh` script.")
    return str(robex_script)


def robex_mask(img: NiftiImage, seed: int = 0) -> NiftiImage:
    _, mask = robex(img, seed)
    return mask


def robex_stripped(img: NiftiImage, seed: int = 0) -> NiftiImage:
    stripped, _ = robex(img, seed)
    return stripped


def robex(img: NiftiImage, seed: int = 0) -> NiftiImagePair:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        robex_script = _find_robex_script()
        tmp_img_fn = td / "img.nii"
        img.to_filename(tmp_img_fn)
        stripped_fn = td / "stripped.nii"
        mask_fn = td / "mask.nii"
        args = [robex_script, tmp_img_fn, stripped_fn, mask_fn, seed]
        str_args = list(map(str, args))
        out = subprocess.run(str_args, capture_output=True)
        if out.returncode != 0:
            msg = f"Nonzero return code {out.returncode}.\n"
            msg += f"ROBEX Output:\n{str(out.stdout)}"
            raise PyRobexError(msg)
        logger.debug(f"ROBEX Output:\n{str(out.stdout)}")
        stripped = NiftiImage.load(stripped_fn)
        mask = NiftiImage.load(mask_fn)
    return stripped, mask
