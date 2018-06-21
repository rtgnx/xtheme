import os
import shutil
import unittest

from xtheme import init_config

class TestCase(unittest.TestCase):

  def setUp(self):
    init_config(os.getenv('XTHEME_DIR'))

  def tearDown(self):
    shutil.rmtree(os.getenv('XTHEME_DIR'))
