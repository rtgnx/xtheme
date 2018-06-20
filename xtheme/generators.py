import toml

from .helpers import fread, fwrite

from jinja2 import Template
from subprocess import check_output
from os import listdir, mkdir, chmod, getenv
from os.path import isfile, isdir, join


XTHEME_DIR   = getenv('XTHEME_DIR', getenv('HOME') + '/.config/xtheme')
HOOKS        = ['pre-apply', 'post-apply']
HOOK_SHEBANG = "#!/bin/sh"
GENERATORS   = XTHEME_DIR + "/generators"

class Generator(object):

  def __init__(self, name, target, template=None):
    self.name = name
    self.target = target

    if template is None and isfile(target):
      with open(target, 'r') as fd:
        self.template = fd.read()

  def save(self):
    root = join(GENERATORS, self.name)
    if not isdir(root):
      mkdir(root, 755)

    for h in HOOKS:
      path = join(root, h + '.sh')
      if not isfile(path):
        fwrite(join(path), HOOK_SHEBANG)
        chmod(path, 755)

    fwrite(join(root, 'config.toml'), self.__toml__())
    fwrite(join(root, 'template.jinja2'), self.template)

  def load(name):
    root = join(GENERATORS, name)
    temp = fread(join(root, 'template.jinja2'))
    conf = toml.loads(fread(join(root, 'config.toml')))

    if 'config' not in conf.keys() or not has_keys(['name', 'target']):
      return None

    return Generator(name=conf['name'], target=conf['target'], template=temp)

  def list():
    return [f for f in listdir(GENERATORS) if isdir(join(GENERATORS, f))]

  def __toml__(self):
    return toml.dumps({'config': {'name': self.name, 'target': self.target}})
    pass

  def apply(self, theme):
    root = join(GENERATORS, self.name)
    out = check_output([join(root, 'pre-apply.sh')])
    res = Template(self.template).render(theme.ctx)
    fwrite(self.target, res)
    out = check_output([join(root, 'post-apply.sh')])
    pass
  pass