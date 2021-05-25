# -*- coding: utf-8 -*-
"""
pyrobex.io

load an image with either antspy or nibabel

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 6, 2021
"""

__all__ = [
    "NiftiImage",
    "NiftiImagePair",
]

import logging
import os
from typing import Tuple

import numpy as np

logger = logging.getLogger(__name__)

ants_flag = os.environ.get("USE_ANTSPY")
if ants_flag is not None:
    use_ants = ants_flag.lower() == "true"
else:
    use_ants = False

if use_ants:
    try:
        import ants

        logger.info("Using antspy as the backend.")
    except (ImportError, ModuleNotFoundError):
        import nibabel as nib

        msg = "USE_ANTSPY set to true, but could not import antspy.\n"
        msg += "Using nibabel as fallback."
        logger.warning(msg)
        use_ants = False
else:
    import nibabel as nib  # noqa

    logger.info("Using nibabel as the backend.")


class NiftiImage:
    """ Helper class to work with nibabel and antspy images """

    def __init__(
        self,
        data: np.ndarray,
        header=None,  # nib.Nifti1Header
        affine: np.ndarray = None,
        extra: dict = None,
    ):
        self.data = data
        self.header = header
        self.affine = affine
        self.extra = extra

    @classmethod
    def load(cls, filename: str):
        if use_ants:
            image = ants.image_read(str(filename))
            return image  # if ants, don't need to bother with this class
        else:
            image = nib.load(filename)
            data = np.asarray(image.get_fdata())  # convert memmap to ndarray
            header = image.header
            affine = image.affine
            extra = image.extra
            return cls(data, header, affine, extra)

    def to_filename(self, filename: str):
        img = self.to_nibabel()
        img.to_filename(filename)

    def to_nibabel(self) -> nib.Nifti1Image:
        return nib.Nifti1Image(self.data, self.affine, self.header, self.extra)


NiftiImagePair = Tuple[NiftiImage, NiftiImage]
