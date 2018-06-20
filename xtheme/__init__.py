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

name = "xtheme"

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
def theme(theme):
  Theme(name=theme).save()

@click.command("generator", help="manange generators")
@click.argument('generator')
@click.option('--target', 'target', default='', help='target config file')
def generator(generator, target):
  Generator(generator, target).save()

@click.command("apply", help="apply theme")
@click.argument("theme")
def apply(theme):

  theme = Theme.load(theme + '.toml')

  if theme is None:
    return

  click.echo("Applying theme %s" % theme.name)

  for gen in Generator.list():
    gen = Generator.load(gen)

    if gen is None:
      continue

    if gen is not None:
      gen.apply(theme)
      click.echo("[+] %s" % gen.name)

@click.command("list", help="list resources")
@click.option("--theme", "theme", is_flag=True, help="List available themes")
@click.option("--gen", "gen", is_flag=True, help="List available generators")
def _list(theme, gen):
  if theme:
    for th in Theme.list():
      click.echo("%s" % th.rsplit('.', 1)[0])
  if gen:
    for g in Generator.list():
      click.echo("%s" % g)

def main():
  cli.add_command(theme)
  cli.add_command(generator)
  cli.add_command(apply)
  cli.add_command(_list)

  cli()
  return 0
