#!/usr/bin/env python2

import unittest
import os
import sys
import copy
from contextlib import contextmanager
from StringIO import StringIO

import combine_cats as ccats
#class TestFitsutils(unittest.TestCase):
#    def test_combine(self):
#        pass

@contextmanager
def capture_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestCobmineCats(unittest.TestCase):
    def test_commandline(self):
        try:
            os.unlink('MyNewCat.fits')
        except:
            pass
        temp = copy.deepcopy(sys.argv)
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'MyNewCat.fits',
                    '--incats',
                    '/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits,/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits']
        with capture_output() as (out, err):
            ccats.main()
            output = out.getvalue().strip()
            self.assertFalse('Removing' in output)

        with capture_output() as (out, err):
            ccats.main()
            output = out.getvalue().strip()
            self.assertTrue('Removing' in output)

        sys.argv = temp

    def test_debug(self):
        try:
            os.unlink('MyNewCat.fits')
        except:
            pass
        temp = copy.deepcopy(sys.argv)
        os.environ['FITSUTILS_DEBUG'] = '10'
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'MyNewCat.fits',
                    '--incats',
                    '/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits,/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits']
        with capture_output() as (out, err):
            ccats.main()
            output = out.getvalue().strip()
            self.assertTrue('fits_close' in output)

        sys.argv = temp

    def test_list_input(self):
        try:
            os.unlink('MyNewCat.fits')
        except:
            pass
        temp = copy.deepcopy(sys.argv)
        with open('mycats.list', 'w') as fh:
            fh.write('/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits\n/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits')
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'MyNewCat.fits',
                    '--list',
                    'mycats.list']
        ccats.main()

        sys.argv = temp

if __name__ == '__main__':
    unittest.main()
