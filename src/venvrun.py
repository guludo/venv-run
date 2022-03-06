from argparse import ArgumentParser, REMAINDER
from collections import OrderedDict
from glob import glob
import os.path
import platform
import re
import subprocess
import sys


def guess():
    if platform.system() != 'Windows':
        pypath = ('bin', 'python')
    else:
        pypath = ('Scripts', 'python.exe')

    exes = []

    exes.extend(glob(os.path.join('*', *pypath)))
    exes.extend(glob(os.path.join('.*', *pypath)))
    exes.append(os.path.join(os.path.curdir, *pypath))
    try:
        with open('.python-version', 'r') as f:
            for prefix in (x.strip() for x in f if not re.match(r'\s*#', x)):
                proc = subprocess.run(
                    ('pyenv', 'prefix', prefix),
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                exes.append(os.path.join(proc.stdout.decode().strip(), *pypath))
                break
    except FileNotFoundError:
        pass

    venvs = OrderedDict(
        # Absolutize, normalize, and canonicalize for deduplication
        (os.path.realpath(os.path.abspath(
            os.path.dirname(os.path.dirname(exe)))), True)
        for exe in exes
        if os.access(exe, os.X_OK)
    )

    return list(venvs.keys())


def run():
    parser = ArgumentParser(
        usage='%(prog)s [OPTIONS] [--] [CMD]',
        description='''
            Run command from an existing python virtual environment (that is,
            with the environment's bin directory prepended to PATH). By default
            the location of the virtual environment directory is searched from
            your current working directory and used if only one match is found.
            This behavior can be overridden with the --venv option.

            CMD contains the command line to execute. You can prepend
            CMD with -- to avoid conflict with %(prog)s own options. If CMD is
            omitted then the environment's python interpreter is run without
            arguments.

            This tool tries to guess if you want to run the python interpreter
            so that you do not need to start CMD with 'python'. For that it
            first tries to run CMD. If that fails because the executable for
            CMD can not be found and the first word of CMD begins with '-' or
            ends with '.py', then 'python' is prepended to CMD and the
            execution is retried. If you do not desire such a behavior, pass
            the --no-guess option.
        ''',
    )

    parser.add_argument('--venv',
        help='''
            Use this virtual environment instead of searching for one.
        ''',
    )

    parser.add_argument('--no-guess',
        action='store_true',
        help='''
            Do not try to prepend 'python' when execution fails because the
            command is not found.
        ''',
    )

    args, cmd_args = parser.parse_known_args()

    if not cmd_args:
        cmd_args = ['python']

    if cmd_args and cmd_args[0] == '--':
        cmd_args.pop(0)
    if not args.venv:
        venvs = guess()

        if not venvs:
            print('No virtual environments found', file=sys.stderr)
            exit(1)

        if len(venvs) > 1:
            print('More than one virtual environment found:', file=sys.stderr)
            for p in venvs:
                print('  ' + p, file=sys.stderr)
            print('Please, use the --venv option.', file=sys.stderr)
            exit(1)

        args.venv = venvs[0]
    path = ''
    if platform.system() != 'Windows':
        path = os.path.join(args.venv, 'bin')
    else:
        path = os.path.join(args.venv, 'Scripts')

    if 'PATH' in os.environ:
        os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
    else:
        os.environ['PATH'] = path

    try:
        os.execvp(cmd_args[0], cmd_args)
    except FileNotFoundError:
        if args.no_guess:
            raise

        if cmd_args[0].startswith('-') or cmd_args[0].endswith('.py'):
            cmd_args.insert(0, 'python')
            os.execvp(cmd_args[0], cmd_args)
        else:
            raise


if __name__ == '__main__':
    run()
