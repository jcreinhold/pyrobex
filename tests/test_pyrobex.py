#!/usr/bin/env python

"""Tests for `pyrobex` package."""

from pathlib import Path
import unittest

import nibabel as nib

from pyrobex.pyrobex import robex, _find_assets


class TestPyrobex(unittest.TestCase):
    """Tests for `pyrobex` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        assets = Path(_find_assets())
        test_file = assets / "ROBEX" / "ref_vols" / "atlas.nii.gz"
        self.test_image = nib.load(test_file)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.test_image

    def test_robex(self):
        """Test robex."""
        stripped, mask = robex(self.test_image)
        stripped_shape = stripped.get_fdata().shape
        mask_shape = mask.get_fdata().shape
        image_shape = self.test_image.get_fdata().shape
        self.assertTupleEqual(stripped_shape, mask_shape)
        self.assertTupleEqual(mask_shape, image_shape)
