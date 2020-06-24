import pathlib
from setuptools import setup, find_packages
from random_proxies.proxies.settings import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name = "random_proxies",
    version = __version__,
    description = "Get a proxy server IP on the fly!",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/2knal/random_proxies",
    author = "Kunal Sonawane",
    author_email = "kunal.sonawane@somaiya.edu",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        "beautifulsoup4>=4.9.0",
        "lxml>=4.5.0",
        "PySocks>=1.7.1",
        "python-dotenv>=0.13.0",
        "requests>=2.23.0"
    ]
)
