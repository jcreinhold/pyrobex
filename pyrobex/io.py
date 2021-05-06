# -*- coding: utf-8 -*-
"""
pyrobex.io

load an image with either antspy or nibabel

Author: Jacob Reinhold (jcreinhold@gmail.com)
Created on: May 6, 2021
"""

import os

from pyrobex.types import NiftiImage

ants_flag = os.environ.get('USE_ANTSPY')
if ants_flag is not None:
    use_ants = ants_flag.lower() == 'true'
else:
    use_ants = False

if use_ants:
    try:
        import ants as backend
    except (ImportError, ModuleNotFoundError):
        import nibabel as backend

        use_ants = False
else:
    import nibabel as backend


def load(filename: str) -> NiftiImage:
    if use_ants:
        image = backend.image_read(filename)
    else:
        image = backend.load(filename)
    return image
