from distutils.core import setup

setup(name='lafourche',
      version='0.0',
      description='La Fourche',
      author='MV&GB',
      packages=[
          'lafourche',
          'lafourche.model',
          'lafourche.parser',
          'lafourche.svg',
          'lafourche.svg.geo',
      ])
