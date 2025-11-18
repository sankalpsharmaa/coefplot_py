"""
Setup script for coefplot_py package
"""

from setuptools import setup, find_packages
import os


# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# Read version from __init__.py
def get_version():
    init_path = os.path.join("coefplot_py", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"


setup(
    name="coefplot-py",
    version=get_version(),
    author="Sankalp Sharma",
    description="Python implementation of Stata's coefplot functionality",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sankalpsharma/coefplot_py",
    packages=find_packages(),
    package_data={
        "coefplot_py": ["*.ado"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "matplotlib>=3.3.0",
        "scipy>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
)
