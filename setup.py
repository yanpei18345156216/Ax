#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

import subprocess

import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.extension import Extension


EXTENSIONS = [
    Extension(
        "ax.utils.stats.sobol",
        ["ax/utils/stats/sobol.pyx"],
        include_dirs=[numpy.get_include()],
    )
]

REQUIRES = [
    "botorch>=0.1.3",
    "jinja2",  # also a Plotly dep
    "pandas",
    "scipy",
    "sklearn",
    "plotly",
]

# pytest-cov requires pytest >= 3.6
DEV_REQUIRES = [
    "beautifulsoup4",
    "black",
    "flake8",
    "pytest>=3.6",
    "pytest-cov",
    "sphinx",
    "sphinx-autodoc-typehints",
]

MYSQL_REQUIRES = ["SQLAlchemy>=1.1.13"]

NOTEBOOK_REQUIRES = ["jupyter"]


def get_git_version(abbreviate: bool = False) -> str:
    """Gets the latest Git tag (as a string), e.g. 0.1.2.

    Note that `git describe --tags` works as follows:
    - Finds the most recent tag that is reachable from a commit.
    - If the tag points to the commit, then only the tag is shown.
    - Otherwise, it suffixes the tag name with the number of additional commits
      on top of the tag, and the abbreviated name of the most recent commit,
      e.g. 0.1.2-9-g2118b21. If you add `--abbrev=0`, this suffix is removed.
      This behavior is controlled by the `abbrev` parameter.
    """
    cmd = ["git", "describe", "--tags"]
    if abbreviate:
        cmd.append("--abbrev=0")
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.strip().decode("ascii")
    except (subprocess.SubprocessError, OSError):
        return "Unknown"


def write_version_py(version: str) -> None:
    """Write the current package version to a Python file (ax/version.py)

    This file will be imported by ax/__init__.py, so that users can determine
    the current version by running `from ax import __version__`.
    """
    content = """#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

# THIS FILE IS GENERATED FROM AX SETUP.PY

version = "%s"
"""
    f = open("ax/version.py", "w")
    try:
        f.write(content % version)
    finally:
        f.close()
    return version


def setup_package() -> None:
    """Used for installing the Ax package.

    First, we determine the current version by getting the latest tag from Git.
    We write this version to a file (ax/version.py), which is imported by
    __init__.py. We also pass this version to setuptools below.
    """

    # Grab current version from Git
    # Abbreviated version (e.g. 0.1.2) will be used by setuptools
    # Unabbreviated version (e.g. 0.1.2-9-g2118b21) will be used by __init__.py
    abbreviated_version = get_git_version(abbreviate=True)
    version = get_git_version(abbreviate=False)

    # Write unabbreviated version to version.py
    write_version_py(version)

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        name="ax-platform",
        version=abbreviated_version,
        description="Adaptive Experimentation",
        author="Facebook, Inc.",
        license="MIT",
        url="https://github.com/facebook/Ax",
        keywords=["Experimentation", "Optimization"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            "Programming Language :: Python :: 3",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        python_requires=">=3.6",
        setup_requires=["cython", "numpy"],
        install_requires=REQUIRES,
        packages=find_packages(),
        ext_modules=cythonize(EXTENSIONS),
        package_data={
            # include all js, css, and html files in the package
            "": ["*.js", "*.css", "*.html"]
        },
        extras_require={
            "dev": DEV_REQUIRES,
            "mysql": MYSQL_REQUIRES,
            "notebook": NOTEBOOK_REQUIRES,
        },
    )


if __name__ == "__main__":
    setup_package()
