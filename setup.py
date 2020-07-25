import setuptools
from meta import version

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kvhf", 
    version=version,
    author="Hugo A",
    author_email="author@example.com",
    long_description_content_type='text/markdown',
    long_description=long_description,
    description="Python package to manipulate kvhf files",
    url="https://github.com/crazyhouse33/kvhf.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.3',
)
