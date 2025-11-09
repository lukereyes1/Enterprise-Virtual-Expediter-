"""Setup script for ShortScreen package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shortscreen",
    version="0.1.0",
    author="ShortScreen Team",
    description="A macro-to-theme-to-target engine for bearish investment ideas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shortscreen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "mypy>=1.0",
            "black>=22.0",
            "flake8>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shortscreen-cli=shortscreen.cli:main",
        ],
    },
    package_data={
        "shortscreen": ["config/*.yaml"],
    },
    include_package_data=True,
)
