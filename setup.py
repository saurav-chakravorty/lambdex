import sys
import codecs
from setuptools import setup, find_packages

import lambdex


def _get_requirements():
    reqs = []

    if sys.version_info < (3, 7):
        reqs.append("dataclasses")

    reqs.append("inquirer==2.7.0")
    return reqs


with codecs.open("README.md", "r", "utf-8") as fd:
    setup(
        name="lambdex",
        version=lambdex.__version__,
        description="A library to write multi-line anonymous functions.",
        long_description=fd.read(),
        license="GPL-3.0 License",
        author="Jingyi Xie (hsfzxjy)",
        author_email="hsfzxjy@gmail.com",
        url="https://github.com/hsfzxjy/lambdex",
        packages=find_packages('.'),
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Software Development :: Compilers",
            "Topic :: Software Development :: Pre-processors",
            "Typing :: Typed",
        ],
        entry_points={
            "console_scripts": [
                "lxfmt = lambdex.fmt.cli.main:main",
                "lxfmt-mock = lambdex.fmt.cli.mock:main"
            ]
        },
        install_requires=_get_requirements(),
    )