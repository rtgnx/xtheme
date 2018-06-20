import os
import sys
import toml
import click
from jinja2 import Template
from subprocess import check_output

from os.path import isdir, isfile, join

# Get config directory from $XTHEME_DIR (default $HOME/.config/xtheme)
XTHEME_DIR = os.getenv('XTHEME_DIR', os.getenv('HOME') + '/.config/xtheme')
THEMES     = XTHEME_DIR + "/themes"
GENERATORS = XTHEME_DIR + "/generators"

GEN_SETTINGS_TEMPLATE = {
  'settings': {
    'name': '%s', 'target': '%s', 'pre-apply': '%s', 'post-apply': '%s'
  }
}

THEME_TEMPLATE = {'colors': {'color%d' % i: '#fff' for i in range(0, 15)}}

if not isdir(XTHEME_DIR):
  os.mkdir(XTHEME_DIR)
  os.mkdir(XTHEME_DIR + "/themes")
  os.mkdir(XTHEME_DIR + "/generators")


def touch(fname, times=None):
  with open(fname, 'a'):
    os.utime(fname, times)

def fread(fpath):
  with open(fname, 'r') as fd:
    return fd.read()

def fwrite(fpath, data):
  with open(fpath, 'w') as fd:
    fd.write(data)

# just becaue I can do it in one line :D
def has_keys(d, keys):
  return len([k for k in keys if k not in d.keys()]) == 0

def list_themes():
  return [f for f in os.listdir(THEMES) if isfile(join(THEMES, f))]

def list_generators():
  return [f for f in os.listdir(GENERATORS) if isdir(join(GENERATORS, f))]

def load_generators():
  gens = {}
  for g in list_generators():
    path = join(GENERATORS, g)
    gens[g] = {'template':  fread(join(GENERATORS, 'template.jinja'))}
    settings = toml.loads(fread(join(GENERATORS, 'settings.toml')))

    gens[g] = {**gens[g], **settings}
    if not has_keys(gens[g], ['name', 'target', 'pre-apply', 'post-apply']):
      del gens[g]
      continue

  return gens


def exec_script(path, stderr=False):
  if not isfile(path):
    return

  out = check_output([path])
  if stderr:
    sys.stderr.write(out)

def apply_theme(theme, gen):
  exec_script(gen['settings']['pre-apply'])
  Template(gen['template'])
  res = Template.render(**theme)
  fwrite(gen['settings']['target'], res)


@click.group()
def cli():
  pass


@click.command()
@click.option('--new', 'new', help='New theme name')
@click.option('--list', 'ls', is_flag=True, help='List themes')
def theme(new, ls):
  if ls:
    for theme in list_themes():
      print("+ %s" % theme)

  if new is None:
    return

  fwrite("%s/%s.toml" % (THEMES, new), toml.dumps(THEME_TEMPLATE))
  pass


@click.command()
@click.option('--new', 'new', help='New generator name')
@click.option('--list', 'ls', is_flag=True, help='List generators')
@click.option('--target', 'target', default='', help='target config file')
def generator(new, ls, target):
  if ls:
    for g in [f for f in os.listdir(GENERATORS) if isdir(join(GENERATORS, f))]:
      print("+ %s" % g)

  if new is None:
    return

  path = "%s/%s" % ( GENERATORS, new)
  os.mkdir(path)

  hooks = ["%s/pre-apply.sh" % path, "%s/post-apply.sh" % path]
  settings = toml.dumps(GEN_SETTINGS_TEMPLATE) % (new, target, *hooks)

  fwrite("%s/%s.toml" % (path, "settings"), settings)
  touch("%s/%s.jinja" % (path, "template"))

  for h in hooks:
    touch(h)
    os.chmod(h, 744)
  pass


@click.command()
@click.option('--theme', 'theme', help='theme to apply')
def apply(theme):
  if theme is None:
    return

  path = "%s/%s.toml" % (THEMES, theme)

  if not isfile(path):
    print("[-] theme %s does not exists" % theme)

  theme = {}

  with open(path, 'r') as fd:
    theme = toml.loads(fd.read())

  for g in load_generators():
    apply_theme(theme, g)


def main():
  cli.add_command(theme)
  cli.add_command(generator)
  cli.add_command(apply)

  cli()
  return 0

if __name__ == "__main__":
  sys.exit(main())
