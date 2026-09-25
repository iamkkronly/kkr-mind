#!/usr/bin/env python3
"""
KKR Mind - Unified AI Interface
Setup configuration for PyPI distribution

Developer / Founder: Kaustav Kanti Ray (@iamkkronly)
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="kkrmind",
    version="1.1.2",
    author="Kaustav Kanti Ray",
    author_email="kkray1345@gmail.com",
    description=(
        "Unified AI interface - one private AI engine with memory and "
        "streaming behind one simple API. No model names exposed."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamkkronly/kkr-mind",
    packages=find_packages(),
    package_data={
        "kkrmind": ["docs.md"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
    ],
    keywords=(
        "ai, llm, chatbot, artificial-intelligence, machine-learning, "
        "streaming, memory"
    ),
    project_urls={
        "Homepage": "https://github.com/iamkkronly/kkr-mind",
        "Repository": "https://github.com/iamkkronly/kkr-mind",
        "PyPI": "https://pypi.org/project/kkrmind/",
    },
    zip_safe=False,
)
