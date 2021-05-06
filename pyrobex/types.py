# -*- coding: utf-8 -*-
"""
pyrobex.types

pyrobex-specific types

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 5, 2021
"""
__all__ = [
    'NiftiImage',
    'NiftiImagePair',
]

from typing import Tuple

import nibabel as nib

NiftiImage = nib.Nifti1Image
NiftiImagePair = Tuple[NiftiImage, NiftiImage]
