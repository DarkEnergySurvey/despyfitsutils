#!/usr/bin/env python3

import unittest
import os
import sys
import copy
import shutil
import filecmp
from contextlib import contextmanager
from io import StringIO

import combine_cats as ccats
import split_head as splith
import despyfitsutils.fits_special_metadata as fsm
from astropy.io import fits
import printHeader as phdr
#class TestFitsutils(unittest.TestCase):
#    def test_combine(self):
#        pass

ROOT = '/var/lib/jenkins/test_data/'

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
    @classmethod
    def setUpClass(cls):
        os.symlink(ROOT + 'cat', 'cat_orig')
        os.symlink(ROOT + 'list', 'list')

    @classmethod
    def tearDownClass(cls):
        os.unlink('cat_orig')
        os.unlink('list')

    def setUp(self):
        shutil.rmtree('cat', ignore_errors=True)
        os.mkdir('cat')

    def tearDown(self):
        shutil.rmtree('cat', ignore_errors=True)

    def test_commandline(self):

        temp = copy.deepcopy(sys.argv)
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'cat/MyNewCat.fits',
                    '--list',
                    'list/combine_cats/combine-cats.list']
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

        temp = copy.deepcopy(sys.argv)
        f = open(ROOT + 'list/combine_cats/combine-cats.list', 'r')
        files = f.readlines()
        f.close()

        inputs = ','.join([f.strip() for f in files])

        os.environ['FITSUTILS_DEBUG'] = '10'
        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'cat/MyNewCat.fits',
                    '--incats',
                    inputs]
        with capture_output() as (out, err):
            ccats.main()
            output = out.getvalue().strip()
            self.assertTrue('fits_close' in output)


        sys.argv = temp

    def test_list_input(self):

        temp = copy.deepcopy(sys.argv)

        sys.argv = ["combine_cats.py",
                    '--outcat',
                    'cat/MyNewCat.fits',
                    '--list',
                    'list/combine_cats/combine-cats.list']
        ccats.main()

        sys.argv = temp


class TestSplitScampHead(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('aux', ignore_errors=True)

    def test_list(self):
        temp = copy.deepcopy(sys.argv)
        shutil.rmtree('aux', ignore_errors=True)
        os.mkdir('aux')
        sys.argv = ['split_head.py',
                    '--in',
                    ROOT + 'aux/scamptest_scamp.head',
                    '--list',
                    ROOT + 'list/split-scamp-head/split-scamp-head.list']
        splith.main()

        f = open(ROOT + 'list/split-scamp-head/split-scamp-head.list', 'r')
        files = f.readlines()
        f.close()
        for f in files:
            name = f.strip()
            self.assertTrue(filecmp.cmp(name, ROOT + name + '.orig', shallow=False))
        sys.argv = temp

    def test_output(self):
        temp = copy.deepcopy(sys.argv)
        shutil.rmtree('aux', ignore_errors=True)
        os.mkdir('aux')
        f = open(ROOT + 'list/split-scamp-head/split-scamp-head.list', 'r')
        files = f.readlines()
        f.close()

        output = ','.join([f.strip() for f in files])

        sys.argv = ['split_head.py',
                    '--in',
                    ROOT + 'aux/scamptest_scamp.head',
                    '--out',
                    output]
        splith.main()

        for f in files:
            name = f.strip()
            self.assertTrue(filecmp.cmp(name, ROOT + name + '.orig', shallow=False))
        sys.argv = temp


class TestFitsSpecialMetadata(unittest.TestCase):
    testfile = ROOT + 'raw/test_raw.fits.fz'
    def test_func_band(self):
        self.assertEqual(fsm.func_band(self.testfile), 'g')
        self.assertEqual(fsm.func_band(self.testfile, fits.open(self.testfile), 'PRIMARY'), 'g')

    def test_func_camsym(self):
        self.assertEqual(fsm.func_camsym(self.testfile), 'D')
        self.assertEqual(fsm.func_camsym(self.testfile, fits.open(self.testfile), 'PRIMARY'), 'D')

    def test_func_nite(self):
        self.assertEqual(fsm.func_nite(self.testfile), '20161018')
        self.assertEqual(fsm.func_nite(self.testfile, fits.open(self.testfile), 'PRIMARY'), '20161018')

    def test_func_objects(self):
        self.assertRaises(KeyError, fsm.func_objects, self.testfile)
        self.assertEqual(fsm.func_objects(self.testfile, fits.open(self.testfile), 1), 4146)
        self.assertEqual(fsm.func_objects(self.testfile, None, 1), 4146)

    def test_func_field(self):
        self.assertEqual(fsm.func_field(self.testfile), '-159-521')
        self.assertEqual(fsm.func_field(self.testfile, fits.open(self.testfile), 'PRIMARY'), '-159-521')
        self.assertRaises(KeyError, fsm.func_field, self.testfile, fits.open(self.testfile), 'PRIM')

    def test_func_radec(self):
        self.assertAlmostEqual(fsm.func_radeg(self.testfile), 345.6291, 4)
        self.assertAlmostEqual(fsm.func_radeg(self.testfile, fits.open(self.testfile), 'PRIMARY'), 345.6291, 4)

    def test_func_tradec(self):
        self.assertAlmostEqual(fsm.func_tradeg(self.testfile), 345.628829, 6)
        self.assertAlmostEqual(fsm.func_tradeg(self.testfile, fits.open(self.testfile)), 345.628829, 6)

    def test_func_decdec(self):
        self.assertAlmostEqual(fsm.func_decdeg(self.testfile), -51.732708, 6)
        self.assertAlmostEqual(fsm.func_decdeg(self.testfile, fits.open(self.testfile), 'PRIMARY'), -51.732708, 6)

    def test_func_tdecdec(self):
        self.assertAlmostEqual(fsm.func_tdecdeg(self.testfile), -51.732137, 6)
        self.assertAlmostEqual(fsm.func_tdecdeg(self.testfile, fits.open(self.testfile)), -51.732137, 6)

class Test_printHeader(unittest.TestCase):
    testfile = ROOT + 'raw/test_raw.fits.fz'
    outfile = 'test.dat'
    def test_main_errors(self):
        temp = copy.deepcopy(sys.argv)
        sys.argv = ['printHeader.py', '-o', '/x/y/z', self.testfile]
        self.assertRaises(SystemExit, phdr.main)

        sys.argv = ['printHeader.py','-x','blob', self.testfile]
        self.assertRaises(OSError, phdr.main)
        sys.argv = copy.deepcopy(temp)

    def test_file_output(self):
        temp = copy.deepcopy(sys.argv)
        sys.argv = ['printHeader.py', '-o', self.outfile, self.testfile]
        phdr.main()
        sys.argv = copy.deepcopy(temp)
        f = open(self.outfile, 'r')
        items = {'SB_ID': False, 'INSTANCE': False, 'SEQID': False}
        for line in f.readlines():
            for key in items.keys():
                if key in line:
                    items[key] = True
                    break
        for key in items.keys():
            self.assertTrue(items[key])
        f.close()
        os.unlink(self.outfile)

    def test_stdout_output(self):
        temp = copy.deepcopy(sys.argv)
        sys.argv = ['printHeader.py', self.testfile]
        output = ''
        with capture_output() as (out, _):
            phdr.main()
            output = out.getvalue().strip()
            items = ['SB_ID', 'INSTANCE','SEQID']
            for it in items:
                self.assertTrue(it in output)

        sys.argv = copy.deepcopy(temp)

if __name__ == '__main__':
    unittest.main()
