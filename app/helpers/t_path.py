import os.path

def t_path(path):
  site_fname = f'{path}'
  global_fname = f'{path}'
  if os.path.isfile(site_fname):
    return site_fname
  else:
    return global_fname

def tp_path(path):
  site_fname = f'sites/current/templates/pages/{path}'
  global_fname = f'pages/{path}'
  if os.path.isfile(site_fname):
    return site_fname
  else:
    return global_fname


