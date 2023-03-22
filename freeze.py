from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], 'include_files':["data_filepaths.confidential"]}

base = 'console'

executables = [
    Executable('driver.py', base=base, target_name = 'Colorshot Automation')
]

setup(name='Colorshot Automation',
      version = '1.0',
      description = 'Automates the consolidation and reporting of raw data files from the ColorshotMS',
      options = {'build_exe': build_options},
      executables = executables)
