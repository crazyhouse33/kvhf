import setuptools
from kvhf.meta import version
import pkgutil
with open("README.md") as fh:
    long_description = fh.read()

packages=setuptools.find_packages()
print ("Found packages:\n",'\n'.join(packages),end='\n\n')
setuptools.setup(
    name="kvhf",
    version=version,
    author="Hugo A",
    author_email="author@example.com",
    scripts=['./kvhf/bin/kvhfplot/kvhfplot', './kvhf/bin/kvhfutils/kvhfutils'],
    long_description_content_type='text/markdown',
    long_description=long_description,
    description="Python package to manipulate kvhf files",
    url="https://github.com/crazyhouse33/kvhf.git",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.3',
    install_requires=[
   'git>=3.1.7',
   'matplotlib>=3.2.2'
    ]
)
