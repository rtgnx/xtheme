import os
import sys
import toml
import click

from os import getenv
from jinja2 import Template
from os.path import isdir, isfile, join
from subprocess import check_output

from .themes import Theme
from .generators import Generator


XTHEME_DIR = getenv('XTHEME_DIR', getenv('HOME') + '/.config/xtheme')

if not isdir(XTHEME_DIR):
  os.mkdir(XTHEME_DIR)
  for d in ['themes', 'generators']:
    if not isdir(join("%s/%s" % (XTHEME_DIR, d))):
      os.mkdir(join("%s/%s" % (XTHEME_DIR, d)))

@click.group()
def cli():
  pass

@click.command("theme", help="manage themes")
@click.argument("theme")
@click.option('--list', 'ls', is_flag=True, help='List themes')
def theme(theme, ls):
  if ls:
    for th in Theme.list():
      click.echo("%s" % th.rstrip(".toml"))
    return

  Theme(name=theme).save()

@click.command("generator", help="manange generators")
@click.argument('generator')
@click.option('--list', 'ls', is_flag=True, help='List generators')
@click.option('--target', 'target', default='', help='target config file')
def generator(generator, ls, target):
  if ls:
    for g in Generator.list():
      click.echo("%s" % g)
    return

  Generator(generator, target).save()

@click.command("apply", help="apply theme")
@click.argument("theme")
def apply(theme):
  theme = Theme.load(theme)

  if theme is None:
    return

  for gen in Generator.list():
    gen = Generator.load(gen)

    if gen is not None:
      gen.apply(theme)

def main():
  cli.add_command(theme)
  cli.add_command(generator)
  cli.add_command(apply)

  cli()
  return 0
