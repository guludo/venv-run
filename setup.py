from setuptools import setup, find_packages

setup(
    name='venv-run',
    version='0.0.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='~=3.5',
)
