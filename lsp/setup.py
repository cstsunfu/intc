# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
from os import PathLike, fspath, path
from platform import system
from tempfile import TemporaryDirectory
from typing import List

from setuptools import find_packages, setup

if sys.platform == "win32":
    sys_post_fix = "win"
elif sys.platform == "darwin":
    sys_post_fix = "mac"
else:
    sys_post_fix = "linux"


def write_version_py():
    with open(os.path.join("intc_lsp", "version.txt")) as f:
        version = f.read().strip()

    # write version info to fairseq/version.py
    with open(os.path.join("intc_lsp", "version.py"), "w") as f:
        f.write('__version__ = "{}"\n'.format(version))
    return version


version = write_version_py()


def build_library(output_path: str, repo_paths: List[str]) -> bool:
    """
    Build a dynamic library at the given path, based on the parser
    repositories at the given paths.

    Returns `True` if the dynamic library was compiled and `False` if
    the library already existed and was modified more recently than
    any of the source files.
    """
    output_mtime = path.getmtime(output_path) if path.exists(output_path) else 0

    if not repo_paths:
        raise ValueError("Must provide at least one language folder")

    cpp = False
    source_paths = []
    for repo_path in repo_paths:
        src_path = path.join(repo_path, "src")
        source_paths.append(path.join(src_path, "parser.c"))
        if path.exists(path.join(src_path, "scanner.cc")):
            cpp = True
            source_paths.append(path.join(src_path, "scanner.cc"))
        elif path.exists(path.join(src_path, "scanner.c")):
            source_paths.append(path.join(src_path, "scanner.c"))
    source_mtimes = [path.getmtime(__file__)] + [
        path.getmtime(path_) for path_ in source_paths
    ]

    if max(source_mtimes) <= output_mtime:
        return False

    # local import saves import time in the common case that nothing is compiled
    try:
        from distutils.ccompiler import new_compiler
        from distutils.unixccompiler import UnixCCompiler
    except ImportError as err:
        raise RuntimeError(
            "Failed to import distutils. You may need to install setuptools."
        ) from err

    compiler = new_compiler()
    if isinstance(compiler, UnixCCompiler):
        compiler.set_executables(compiler_cxx="c++")

    with TemporaryDirectory(suffix="tree_sitter_language") as out_dir:
        object_paths = []
        for source_path in source_paths:
            if system() == "Windows":
                flags = None
            else:
                flags = ["-fPIC"]
                if source_path.endswith(".c"):
                    flags.append("-std=c11")
            object_paths.append(
                compiler.compile(
                    [source_path],
                    output_dir=out_dir,
                    include_dirs=[path.dirname(source_path)],
                    extra_preargs=flags,
                )[0]
            )
        compiler.link_shared_object(
            object_paths,
            output_path,
            target_lang="c++" if cpp else "c",
        )
    return True


build_library(
    os.path.join("intc_lsp", "lib", f"json_{sys_post_fix}_ts.so"),
    [os.path.join("intc_lsp", "csrc", "json")],
)
build_library(
    os.path.join("intc_lsp", "lib", f"yaml_{sys_post_fix}_ts.so"),
    [os.path.join("intc_lsp", "csrc", "yaml")],
)

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license = f.read()

setup(
    version=version,
    url="https://github.com/cstsunfu/intc",
)
