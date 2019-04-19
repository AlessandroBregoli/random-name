import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randomnames",
    version="0.0.1",
    author=["Alessandro Bregoli"],
    author_email=["alessandroxciv@gmail.com"],
    description="Generator of random numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlessandroBregoli/randomnames",
    packages=["randomnames"],
    scripts=["scripts/rndnames"],
    package_data={'randomnames': ['data/*','data/names/*']},
    install_requires=[
        "wheel",
        "numpy",
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
