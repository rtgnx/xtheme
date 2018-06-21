import os
import click
import unittest

os.environ['XTHEME_DIR'] = '/tmp/xtheme'

from xtheme import _list, theme, XTHEME_DIR, init_config
from click.testing import CliRunner

from os.path import isfile, join

from .testcase import TestCase

class ThemeTest(TestCase):

  def create_theme(self, name):
    runner = CliRunner()
    result = runner.invoke(theme, [name])

  def test_list_theme(self):
    runner = CliRunner()
    result = runner.invoke(_list, ['--theme'])
    assert result.output.rstrip() == ''

    self.create_theme('abc')

    assert 'abc' in runner.invoke(_list, ['--theme']).output.splitlines()

  def test_create_theme(self):
    runner = CliRunner()
    result = runner.invoke(theme, ['abcdef'])
    assert result.output == ''
    assert result.exit_code == 0

    assert isfile(join(join(XTHEME_DIR, 'themes'), 'abcdef.toml')) == True
