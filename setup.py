from setuptools import setup

setup(name='miniwizpl',
      version='0.1',
      description='miniWizPL library & compiler for writing zero-knowledge statements',
      url='none',
      author='Joe Near',
      author_email='jnear@uvm.edu',
      license='GPLv3',
      packages=['miniwizpl'],
      install_requires=[], # TODO: add deps
      package_data={'': ['boilerplate/*']},
      include_package_data=True,
      zip_safe=False)
