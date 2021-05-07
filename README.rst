=======
pyrobex
=======

.. image:: https://img.shields.io/pypi/v/pyrobex.svg
        :target: https://pypi.python.org/pypi/pyrobex

.. image:: https://api.travis-ci.com/jcreinhold/pyrobex.svg
        :target: https://travis-ci.com/github/jcreinhold/pyrobex

.. image:: https://readthedocs.org/projects/pyrobex/badge/?version=latest
        :target: https://pyrobex.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Python bindings for `ROBEX`_ brain extraction.

This package comes with ROBEX v1.2 for Linux. Windows is not currently supported.

* Free software: BSD license
* Documentation: https://pyrobex.readthedocs.io.

Install
-------

The easiest way to install the package is with::

    pip install pyrobex

Alternatively, you can download the source and run::

    python setup.py install

Basic Usage
-----------

This package provides a CLI (to the CLI) of ROBEX for convenience and
testing which can be accessed through, e.g.,::

    robex path/to/t1w_image.nii path/to/stripped.nii path/to/mask.nii

The real use-case of this package is by importing robex and using it within
another script or neuroimaging pipeline, e.g.,::

    import nibabel as nib
    from pyrobex.robex import robex
    image = nib.load('path/to/t1w_image.nii')
    stripped, mask = robex(image)

.. _ROBEX: https://www.nitrc.org/projects/robex
