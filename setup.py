from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
product_name = 'Travian Legends Bot'
bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % (product_name),
}

include_files = ['config.json', 'data']

buildOptions = dict(
    packages=['travianapi', 'travianbot'],
    excludes=[],
    includes=['travianapi', 'travianbot', 'queue'],
    include_files=include_files)

import sys

base = 'Win32GUI' if sys.platform == 'win32' else None
targetName = 'travianbot'
if sys.platform == 'win32':
    targetName += '.exe'

executables = [
    Executable('bot_gui_qt5.py',
               base=base,
               targetName=targetName,
               icon="data/images/icon.ico")
]

setup(name='Travian Legends Bot',
      version='0.1.0',
      description='Bot for Travian Legends Browser Game',
      options=dict(bdist_msi=bdist_msi_options, build_exe=buildOptions),
      executables=executables)
