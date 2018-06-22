import toml

from .helpers import fread, fwrite, has_keys

from jinja2 import Template
from subprocess import check_output
from os import listdir, mkdir, makedirs, chmod, getenv
from os.path import isfile, isdir, join, split, expandvars


XTHEME_DIR   = getenv('XTHEME_DIR', getenv('HOME') + '/.config/xtheme')
HOOKS        = ['pre-apply', 'post-apply']
HOOK_SHEBANG = "#!/bin/sh"
GENERATORS   = XTHEME_DIR + "/generators"

class Generator(object):

  def __init__(self, name, target, conf={}, template=None):
    self.name = name
    self.conf = conf
    self.target = target
    self.template = template

    if self.template is None and isfile(target):
      with open(target, 'r') as fd:
        self.template = fd.read()

    elif self.template is None:
      self.template = ''

  def save(self):
    root = join(GENERATORS, self.name)
    if not isdir(root):
      mkdir(root, 0o744)

    for h in HOOKS:
      path = join(root, h + '.sh')
      if not isfile(path):
        fwrite(join(path), HOOK_SHEBANG)
        chmod(path, 0o744)

    fwrite(join(root, 'config.toml'), self.__toml__())
    fwrite(join(root, 'template.jinja2'), self.template)

  def load(name):
    root = join(GENERATORS, name)
    temp = fread(join(root, 'template.jinja2'))

    if temp is None:
      printf("[-] Template file missing in: %s" % name)
      return None

    config = toml.loads(expandvars(fread(join(root, 'config.toml'))))

    if 'config' not in config.keys():
      print("[-] Invalid config file in: %s" % name)
      return None

    conf = config['config']
    if not has_keys(conf, ['name', 'target']):
      return None

    return Generator(conf['name'], conf['target'], conf=config, template=temp)

  def list():
    return [f for f in listdir(GENERATORS) if isdir(join(GENERATORS, f))]

  def __toml__(self):
    return toml.dumps({'config': {'name': self.name, 'target': self.target}})
    pass

  def apply(self, theme):
    ctx = {**self.conf, **theme.ctx}
    root = join(GENERATORS, self.name)
    out = check_output([join(root, 'pre-apply.sh')], cwd=root)
    res = Template(expandvars(self.template)).render(ctx)
    fwrite(self.target, res)

    if 'targets' in self.conf.keys() and type(self.conf['targets']) == dict:
      for k, v in self.conf['targets'].items():
        res = None
        try:
          res = Template(fread(join(root, k + '.jinja2'))).render(ctx)
        except:
          print("[-] Unable to compile %s.jinja2" % k)
          continue

        try:
          fwrite(v, res)
        except FileNotFoundError:
          path, fname = split(v)
          makedirs(path, 0o744)

        finally:
          fwrite(v, res)

    out = check_output([join(root, 'post-apply.sh')], cwd=root)
    pass
  pass
