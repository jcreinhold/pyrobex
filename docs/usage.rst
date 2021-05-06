=====
Usage
=====

To use pyrobex in a project::

    import pyrobex

Then you can do skull-strip NIfTI images from ANTsPy or Nibabel, e.g. ::

    import nibabel as nib
    image = nib.load('path/to/image.nii.gz')
    stripped, mask = pyrobex.robex(image)

Console script
~~~~~~~~~~~~~~

.. argparse::
   :module: pyrobex.cli
   :func: arg_parser
   :prog: robex
