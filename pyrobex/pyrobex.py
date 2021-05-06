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

import nibabel as nib

from pyrobex.errors import PyRobexError
from pyrobex.types import NiftiImage, NiftiImagePair

logger = logging.getLogger(__name__)


def _find_assets() -> str:
    file_path = Path(__file__).resolve()
    pyrobex_dir = file_path.parents[1]
    assets = pyrobex_dir / "assets"
    return str(assets)


def _find_robex_script() -> str:
    assets = Path(_find_assets())
    robex_script = assets / "ROBEX" / "runROBEX.sh"
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
            msg += "ROBEX Output:\n"
            msg += str(out.stdout)
            raise PyRobexError(msg)
        stripped = nib.load(stripped_fn)
        mask = nib.load(mask_fn)
    return stripped, mask
