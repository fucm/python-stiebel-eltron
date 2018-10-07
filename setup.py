"""
Copyright (c) 2018 Martin Fuchs <martin.fuchs@gmx.ch>
Licensed under MIT. All rights reserved.
"""
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name='pystiebeleltron',
    version='0.0.1.dev0',
    description='Python API for interacting with the Stiebel Eltron ISG web gateway via Modbus for controlling integral ventilation units and heat pumps.',
    long_description=long_description,
    url='https://github.com/fucm/python-stiebel-eltron',
    author='Martin Fuchs',
    author_email='martin.fuchs@gmx.ch',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
