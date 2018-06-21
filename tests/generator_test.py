import os
import click
import unittest

os.environ['XTHEME_DIR'] = '/tmp/xtheme'

from xtheme import XTHEME_DIR
from click.testing import CliRunner

from os.path import isfile, join

from .testcase import TestCase

class GeneratorTest(TestCase):
  pass
