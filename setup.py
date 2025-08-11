#!/usr/bin/env python3
"""
Setup configuration for filesystem-server.
"""

from setuptools import setup

setup(
    name="filesystem-server",
    version="0.1.0",
    description="MCP server for filesystem access with command-line configuration",
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
    author="FileSystem MCP Server",
    long_description="A Model Context Protocol (MCP) server that provides secure filesystem access for AI assistants, configured entirely via command-line arguments.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)