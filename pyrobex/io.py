# -*- coding: utf-8 -*-
"""
pyrobex.io

load an image with either antspy or nibabel

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 6, 2021
"""

__all__ = [
    'NiftiImage',
    'NiftiImagePair',
]

import os
from typing import Tuple

import numpy as np

ants_flag = os.environ.get('USE_ANTSPY')
if ants_flag is not None:
    use_ants = ants_flag.lower() == 'true'
else:
    use_ants = False

if use_ants:
    try:
        import ants
    except (ImportError, ModuleNotFoundError):
        import nibabel as nib

        use_ants = False
else:
    import nibabel as nib


class NiftiImage:
    def __init__(self,
                 data: np.ndarray,
                 header: nib.Nifti1Header = None,
                 affine: np.ndarray = None,
                 extra: dict = None):
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
        img = nib.Nifti1Image(self.data, self.affine, self.header, self.extra)
        img.to_filename(filename)


NiftiImagePair = Tuple[NiftiImage, NiftiImage]
