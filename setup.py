from setuptools import find_packages
from setuptools import setup

install_requires = [
  'numpy',
  'scipy',
]

tests_require = [
  'pytest',
]

setup(name='pyAudioGraphInput',
      version='0.1',
      description='Python Audio Graph Input',
      author='Bruno Di Giorgi',
      author_email='bruno@brunodigiorgi.it',
      url='https://github.com/brunodigiorgi/pyAudioGraphInput',
      license="GPLv2",
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
        'testing': tests_require,
      },
      )
