from __future__ import unicode_literals

import contextlib
import functools
import hashlib
import os
import os.path
import shutil
import sys
import tarfile
import tempfile


def memoize_by_cwd(func):
    """Memoize a function call based on os.getcwd()."""
    @functools.wraps(func)
    def wrapper(*args):
        cwd = os.getcwd()
        key = (cwd,) + args
        try:
            return wrapper._cache[key]
        except KeyError:
            ret = wrapper._cache[key] = func(*args)
            return ret

    wrapper._cache = {}

    return wrapper


def entry(func):
    """Allows a function that has `argv` as an argument to be used as a
    commandline entry.  This will make the function callable using either
    explicitly passed argv or defaulting to sys.argv[1:]
    """
    @functools.wraps(func)
    def wrapper(argv=None):
        if argv is None:
            argv = sys.argv[1:]
        return func(argv)
    return wrapper


@contextlib.contextmanager
def clean_path_on_failure(path):
    """Cleans up the directory on an exceptional failure."""
    try:
        yield
    except BaseException:
        if os.path.exists(path):
            shutil.rmtree(path)
        raise


@contextlib.contextmanager
def noop_context():
    yield


def shell_escape(arg):
    return "'" + arg.replace("'", "'\"'\"'".strip()) + "'"


def hex_md5(s):
    """Hexdigest an md5 of the string.

    :param text s:
    """
    return hashlib.md5(s.encode('utf-8')).hexdigest()


@contextlib.contextmanager
def tarfile_open(*args, **kwargs):
    """Compatibility layer because python2.6"""
    tf = tarfile.open(*args, **kwargs)
    try:
        yield tf
    finally:
        tf.close()


@contextlib.contextmanager
def tmpdir():
    """Contextmanager to create a temporary directory.  It will be cleaned up
    afterwards.
    """
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)
