=====
Usage
=====

To use pyrobex in a project::

    from pyrobex.robex import robex

Then you can skull-strip NIfTI images from ANTsPy or Nibabel, e.g. ::

    import nibabel as nib
    image = nib.load('path/to/image.nii.gz')
    stripped, mask = robex(image)

Console script
~~~~~~~~~~~~~~

.. argparse::
   :module: pyrobex.cli
   :func: arg_parser
   :prog: robex
