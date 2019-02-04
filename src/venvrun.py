from argparse import ArgumentParser, REMAINDER
from glob import glob
import os.path
import sys

def run():
    parser = ArgumentParser(
        usage='%(prog)s [OPTIONS] [--] [PYTHON_OPTIONS]',
        description='''
            Run python from an existing virtual environment. By default the
            location of the virtual environment directory is searched based
            from your current working directory and used if only one match is
            found. This behavior can be overridden with the --venv option.

            The options passed in PYTHON_OPTIONS are forwarded to the
            environment's python interpreter. You can prepend PYTHON_OPTIONS
            with -- to avoid conflict with
            %(prog)s own options.
        ''',
    )

    parser.add_argument('--venv',
        help='''
            Use this virtual environment instead of searching for one.
        ''',
    )

    args, python_args = parser.parse_known_args()

    if python_args and python_args[0] == '--':
        python_args.pop(0)

    if not args.venv:
        venvs = []
        for p in glob(os.path.join('*', 'bin', 'python')):
            if os.access(p, os.X_OK):
                venvs.append(os.path.dirname(os.path.dirname(p)))

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

    path = os.path.join(args.venv, 'bin')
    if 'PATH' in os.environ:
        os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
    else:
        os.environ['PATH'] = path

    python_args.insert(0, 'python')
    os.execvp('python', python_args)


if __name__ == '__main__':
    run()
