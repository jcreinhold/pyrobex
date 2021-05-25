#!/usr/bin/env python
"""Tests for `pyrobex` package."""

from pathlib import Path
import os

import nibabel as nib
import pytest

from pyrobex.robex import robex, _find_robex_dir
from pyrobex.cli import main


@pytest.fixture
def test_file() -> Path:
    robex_dist = Path(_find_robex_dir())
    test_file = robex_dist / "ref_vols" / "atlas.nii.gz"
    return test_file


@pytest.fixture
def test_image(test_file: Path) -> nib.Nifti1Image:
    return nib.load(test_file)


@pytest.mark.skipif(os.name == "posix", reason="Mac OS X not currently supported.")
def test_robex(test_image: nib.Nifti1Image):
    stripped, mask = robex(test_image)
    stripped_shape = stripped.get_fdata().shape  # noqa
    mask_shape = mask.get_fdata().shape  # noqa
    image_shape = test_image.get_fdata().shape  # noqa
    assert stripped_shape == mask_shape
    assert mask_shape == image_shape


@pytest.fixture(scope="session")
def temp_dir(tmpdir_factory) -> Path:
    return Path(tmpdir_factory.mktemp("out"))


@pytest.mark.skipif(os.name == "posix", reason="Mac OS X not currently supported.")
def test_cli(test_file: Path, temp_dir: Path):
    out_stripped = temp_dir / "stripped.nii"
    out_mask = temp_dir / "mask.nii"
    args = f"{test_file} -os {out_stripped} -om {out_mask}".split()
    retcode = main(args)
    assert retcode == 0
