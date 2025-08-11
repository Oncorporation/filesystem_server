#!/usr/bin/env python3
"""
Setup configuration for filesystem-server.
"""

from setuptools import setup

setup(
    name="filesystem-server",
    version="0.1.0",
    description="MCP server for filesystem access with configurable directory and file type restrictions",
    py_modules=["app"],
    python_requires=">=3.10",
    install_requires=[
        "fastmcp",
    ],
    entry_points={
        "console_scripts": [
            "filesystem-server=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config.json"],
    },
)