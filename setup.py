"""
Copyright (c) 2018 Martin Fuchs <martin.fuchs@gmx.ch>
Licensed under MIT. All rights reserved.
"""
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if sys.argv[-1] == 'build':
    os.system('python3 setup.py sdist bdist_wheel')
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system('twine upload dist/*')
    sys.exit()


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name='pystiebeleltron',
    version='0.0.1.dev2',
    description='Python API for interacting with the Stiebel Eltron ISG web gateway via Modbus for controlling integral ventilation units and heat pumps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fucm/python-stiebel-eltron',
    author='Martin Fuchs',
    license='MIT',
    python_requires='>=3.4',
    install_requires=['pymodbus>=2.1.0'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
