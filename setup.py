from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('bot_gui_qt5.py', base=base, targetName = 'travianbot')
]

setup(name='Travian Legends Bot',
      version = '0.1.0',
      description = 'Bot for Travian Legends Browser Game',
      options = dict(build_exe = buildOptions),
      executables = executables)
