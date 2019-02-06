from setuptools import setup, find_packages

setup(
    name='venv-run',
    version='0.0.0',
    author='Gustavo José de Sousa',
    author_email='gustavo.jo.sousa@gmail.com',
    package_dir={'': 'src'},
    py_modules=['venvrun'],
    python_requires='~=3.5',
    entry_points={
        'console_scripts': [
            'venv-run = venvrun:run',
        ]
    },
)
