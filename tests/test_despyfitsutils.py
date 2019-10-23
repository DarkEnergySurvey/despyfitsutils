#!/usr/bin/env python2

import unittest
import sys
import copy

import combine_cats as ccats
#class TestFitsutils(unittest.TestCase):
#    def test_combine(self):
#        pass

class TestCobmineCats(unittest.TestCase):
    def test_commandline(self):
        temp = copy.deepcopy(sys.argv)
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'MyNewCat.fits',
                    '--incats',
                    '/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits,/var/lib/jenkins/test_data/cat/D00526117_r_c23_r4048p01_scampcat.fits']
        ccats.main()
        sys.argv = temp

if __name__ == '__main__':
    unittest.main()
