import os
import click

os.environ['XTHEME_DIR'] = '/tmp/xtheme'

from xtheme import _list, theme
from click.testing import CliRunner

def test_list_theme():
  runner = CliRunner()
  result = runner.invoke(_list, ['--theme'])
  assert result.output.rstrip() == ''
