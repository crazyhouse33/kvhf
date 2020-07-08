import setuptools
version="0.0.0"

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kvhf", # Replace with your own username
    version=version,
    author="Alonso Hugo",
    author_email="author@example.com",
    description="Python package to manipulate kvhf files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crazyhouse33/kvhf.git",
    packages=setuptools.find_packages(),
    test_suite="tests",   
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
