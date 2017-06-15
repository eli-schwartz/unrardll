#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: BSD Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import absolute_import, division, print_function, unicode_literals

import glob
import os
import re
import sys

from setuptools import Extension, setup

self_path = os.path.abspath(__file__)
base = os.path.dirname(self_path)
iswindows = hasattr(sys, 'getwindowsversion')
raw = open(os.path.join(base, 'src/unrardll/__init__.py'), 'rb').read().decode('utf-8')
version = map(int, re.search(r'^version = V\((\d+), (\d+), (\d+)', raw, flags=re.M).groups())


def include_dirs():
    ans = []
    if 'UNRAR_INCLUDE' in os.environ:
        ans.extend(os.environ['UNRAR_INCLUDE'].split(os.pathsep))
    return ans


def libraries():
    return ['unrar']


def library_dirs():
    ans = []
    if 'UNRAR_LIBDIRS' in os.environ:
        ans.extend(os.environ['UNRAR_LIBDIRS'].split(os.pathsep))
    return ans


def src_files():
    return glob.glob(os.path.join(base, 'src', 'unrardll', '*.cpp'))


def macros():
    ans = [
        ('SILENT', 1),
        ('RARDLL', 1),
        ('UNRAR', 1),
    ]
    if not iswindows:
        ans.append(('_UNIX', 1))
    return ans


CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Archiving :: Compression
"""

setup(
    name=str('unrardll'),
    version='{}.{}.{}'.format(*version),
    author='Kovid Goyal',
    author_email='redacted@acme.com',
    description='Wrap the Unrar DLL to enable unraring of files in python',
    license='BSD',
    url='https://github.com/kovidgoyal/unrardll',
    classifiers=[c for c in CLASSIFIERS.split("\n") if c],
    platforms=['any'],
    packages=['unrardll'],
    package_dir={'': 'src'},
    ext_modules=[
        Extension(
            str('unrardll.unrar'),
            include_dirs=include_dirs(),
            libraries=libraries(),
            library_dirs=library_dirs(),
            define_macros=macros(),
            sources=list(map(str, src_files())))])