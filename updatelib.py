#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import shutil
import tempfile

VERSION = 'nightly'
API_URL = 'https://ampl.com/builds/upload/releases/amplapi/2020-02-27/api/nightly/libampl.zip'
# API_URL = 'http://ampl.com/dl/API/future/{}/libampl.zip'.format(VERSION)


def updatelib():
    from zipfile import ZipFile
    try:
        from urllib import urlretrieve
    except Exception:
        from urllib.request import urlretrieve

    os.chdir(os.path.dirname(__file__) or os.curdir)

    tmpfile = tempfile.mktemp('.zip')
    tmpdir = os.path.join(os.curdir, 'tmp', 'libampl')
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

    print("Downloading:", API_URL)
    urlretrieve(API_URL, tmpfile)
    with ZipFile(tmpfile) as zp:
        zp.extractall(tmpdir)
    try:
        os.remove(tmpfile)
    except Exception:
        pass

    include_dir = os.path.join(tmpdir, 'include', 'ampl')
    intel32 = os.path.join(tmpdir, 'intel32')
    amd64 = os.path.join(tmpdir, 'amd64')
    ppc64le = os.path.join(tmpdir, 'ppc64le')
    wrapper_dir = os.path.join(tmpdir, 'python')
    libs = [('intel32', intel32), ('amd64', amd64), ('ppc64le', ppc64le)]

    amplpy_include = os.path.join('amplpy', 'amplpython', 'cppinterface', 'include', 'ampl')
    try:
        shutil.rmtree(amplpy_include)
    except Exception:
        pass
    shutil.copytree(include_dir, amplpy_include)
    print(
        '*\n!.gitignore\n',
        file=open(os.path.join(amplpy_include, '.gitignore'), 'w')
    )

    print('wrapper:')
    for filename in os.listdir(wrapper_dir):
        print('\t{}'.format(filename))
        shutil.copyfile(
            os.path.join(wrapper_dir, filename),
            os.path.join('amplpy', 'amplpython', 'cppinterface', filename)
        )

    for libname, lib in libs:
        dstdir = os.path.join('amplpy', 'amplpython', 'cppinterface', libname)
        try:
            shutil.rmtree(dstdir)
            os.mkdir(dstdir)
        except Exception:
            pass
        print(
            '*\n!.gitignore\n',
            file=open(os.path.join(dstdir, '.gitignore'), 'w')
        )
        print('{}:'.format(libname))
        for filename in os.listdir(lib):
            if filename.endswith('.jar'):
                continue
            if 'java' in filename:
                continue
            if 'csharp' in filename:
                continue
            print('\t{}'.format(filename))
            shutil.copyfile(
                os.path.join(lib, filename),
                os.path.join(dstdir, filename)
            )


if __name__ == '__main__':
    updatelib()
