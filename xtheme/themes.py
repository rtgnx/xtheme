import toml

from os import listdir, getenv
from os.path import isfile, join

from .helpers import fwrite, fread, dotdict

XTHEME_DIR   = getenv('XTHEME_DIR', getenv('HOME') + '/.config/xtheme')
THEMES = XTHEME_DIR + "/themes"

class Theme(object):

  def __init__(self, name, ctx=None):
    self.name = name
    self.ctx = ctx

  def save(self):
    fwrite(join(THEMES, self.name), self.__toml__())

  def load(name):
    t = fread(join(THEMES, name))

    if t is None:
      return t

    t = toml.loads(t)

    return Theme(name=name.rsplit('.', 1)[0], ctx=dotdict(t))

  def list():
    return [f for f in listdir(THEMES) if isfile(join(THEMES, f))]

  def __toml__(self):
    return toml.dumps({'theme': {'name': self.name}})
