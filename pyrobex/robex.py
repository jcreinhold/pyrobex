# -*- coding: utf-8 -*-
"""
pyrobex.robex

main python wrapper functions for robex

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 5, 2021
"""

__all__ = [
    "robex",
    "robex_mask",
    "robex_stripped",
]

import logging
import subprocess
import tempfile
from pathlib import Path

from pyrobex.errors import PyRobexError
from pyrobex.io import NiftiImage, NiftiImagePair

logger = logging.getLogger(__name__)


def _find_robex_dir() -> str:
    """finds the ROBEX source code directory"""
    file_path = Path(__file__).resolve()
    pyrobex_dir = file_path.parent
    robex_dist = pyrobex_dir / "ROBEX"
    return str(robex_dist)


def _find_robex_script() -> str:
    """finds the ROBEX shell script"""
    robex_dist = Path(_find_robex_dir())
    robex_script = robex_dist / "runROBEX.sh"
    if not robex_script.is_file():
        raise PyRobexError("Could not find `runROBEX.sh` script.")
    return str(robex_script)


def robex_mask(image: NiftiImage, seed: int = 0) -> NiftiImage:
    """
    Takes a NIfTI image from nibabel or antspy and performs
    ROBEX brain extraction on the image volume and returns
    only the mask

    Args:
        image (NiftiImage): a nibabel NIfTI image, e.g.,
            nib.Nifti1Image, or an antspy image
        seed (int): random seed for reproducibility

    Returns:
        mask (NiftiImage): depending on the input,
            returns a nibabel NIfTI image or an antspy
            image of a binary mask of the brain

    Raises:
        PyRobexError: when ROBEX is not found or fails
    """
    _, mask = robex(image, seed)
    return mask


def robex_stripped(image: NiftiImage, seed: int = 0) -> NiftiImage:
    """
    Takes a NIfTI image from nibabel or antspy and performs
    ROBEX brain extraction on the image volume and returns
    only the extracted brain image

    Args:
        image (NiftiImage): a nibabel NIfTI image, e.g.,
            nib.Nifti1Image, or an antspy image
        seed (int): random seed for reproducibility

    Returns:
        stripped (NiftiImage): depending on the input,
            returns a nibabel NIfTI image or an antspy
            image of the extracted brain

    Raises:
        PyRobexError: when ROBEX is not found or fails
    """
    stripped, _ = robex(image, seed)
    return stripped


def robex(image: NiftiImage, seed: int = 0) -> NiftiImagePair:
    """
    Takes a NIfTI image from nibabel or antspy and performs
    ROBEX brain extraction on the image volume

    Args:
        image (NiftiImage): a nibabel NIfTI image, e.g.,
            nib.Nifti1Image, or an antspy image
        seed (int): random seed for reproducibility

    Returns:
        stripped (NiftiImage): depending on the input,
            returns a nibabel NIfTI image or an antspy
            image of the extracted brain
        mask (NiftiImage): depending on the input,
            returns a nibabel NIfTI image or an antspy
            image of a binary mask of the brain

    Raises:
        PyRobexError: when ROBEX is not found or fails
    """
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        robex_script = _find_robex_script()
        tmp_img_fn = tdp / "img.nii"
        image.to_filename(str(tmp_img_fn))
        stripped_fn = tdp / "stripped.nii"
        mask_fn = tdp / "mask.nii"
        args = [robex_script, tmp_img_fn, stripped_fn, mask_fn, seed]
        str_args = list(map(str, args))
        out = subprocess.run(str_args, capture_output=True)
        if out.returncode != 0:
            msg = f"Nonzero return code {out.returncode}.\n"
            msg += f"ROBEX Output:\n{str(out.stdout)}"
            raise PyRobexError(msg)
        logger.debug(f"ROBEX Output:\n{str(out.stdout)}")
        stripped = NiftiImage.load(str(stripped_fn))
        mask = NiftiImage.load(str(mask_fn))
    return stripped, mask
