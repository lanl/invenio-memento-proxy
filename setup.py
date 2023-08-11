__author__ = 'Lyudmila Balakireva'
import os
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='timegate',
      version='0.2.1',
      author_email='ludab@lanl.gov',
      url='',
      download_url='',
      description="A  Memento Proxy for Invenio",
      long_description=read('README.md'),
      packages=find_packages(exclude=['doc.*']),
      keywords='proxy memento uwsgi python',
      license='',
      install_requires=[
          'uWSGI>=2.0.3',
          'ConfigParser>=3.3.0r2',
          'python-dateutil>=2.1',
          'requests>=2.2.1',
          'werkzeug>=0.9.6'

      ],
      include_package_data=True,
      zip_safe=False
      )
