from setuptools import setup, find_packages
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
  name='ezcaptcha',
  version="1.4",
  description="EzCaptcha python sdk",
  long_description=read_file('README.md'),
  long_description_content_type="text/markdown",
  license="MIT",
  keywords='EzCaptcha python sdk',
  author='EzCaptcha',
  author_email='dev@ez-captcha.com',
  url='https://github.com/ez-captcha/ezcaptcha-python',
  classifiers=['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Natural Language :: English',
               'Operating System :: POSIX :: Linux',
               'Programming Language :: Python :: 3.9'
  ],
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  include_package_data=True,
)