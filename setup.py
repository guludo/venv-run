from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="venv-run",
    version="0.2.0",
    author="Gustavo José de Sousa",
    author_email="gustavo.jo.sousa@gmail.com",
    description="Run commands using Python virtual environment",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/guludo/venv-run",
    project_urls={
        "Changelog": "https://github.com/guludo/venv-run/blob/master/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    py_modules=["venvrun"],
    python_requires="~=3.7",
    entry_points={
        "console_scripts": [
            "venv-run = venvrun:run",
        ]
    },
    extras_require={
        "dev": [
            "mypy==1.8.0",
            "nox",
            "types-setuptools",
            "ruff==0.1.12",
        ],
    },
)
