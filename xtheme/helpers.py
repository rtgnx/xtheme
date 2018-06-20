from os.path import isfile, isdir, join

def fread(path):
  if not isfile(path):
    return None

  with open(path, 'r') as fd:
    return fd.read()

def fwrite(path, data):
  with open(path, 'w') as fd:
    return fd.write(data)

def has_keys(d, keys):
  return len([k for k in keys if k not in d.keys()]) == 0

class dotdict(dict):
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
