# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

import os

from setuptools import find_packages, setup


def write_version_py():
    with open(os.path.join("intc", "version.txt")) as f:
        version = f.read().strip()

    # write version info to fairseq/version.py
    with open(os.path.join("intc", "version.py"), "w") as f:
        f.write('__version__ = "{}"\n'.format(version))
    return version


version = write_version_py()


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    license = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read()

pkgs = [p for p in find_packages() if p.startswith("intc")]

setup(
    name="intc",
    version=version,
    url="https://github.com/cstsunfu/intc",
    description="intc: intelligent python config toolkit",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Apache Software License",
    author="cstsunfu",
    author_email="cstsunfu@gmail.com",
    python_requires=">=3.8",
    include_package_data=True,
    packages=pkgs,
    install_requires=requirements.strip().split("\n"),
)
