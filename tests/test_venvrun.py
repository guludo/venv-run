import os
import platform
import subprocess
import sys
import tempfile
import unittest
from subprocess import CompletedProcess, run as real_subprocess_run
from typing import Any
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'src'))
import venvrun


class VenvRunTest(unittest.TestCase):

    def setUp(self) -> None:
        self.oldcwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(__file__), 'fixture'))

    def tearDown(self) -> None:
        os.chdir(self.oldcwd)

    def testGuess(self) -> None:

        def mock_run(*args: Any, **kwargs: Any) -> CompletedProcess[str]:
            if args[0] == ('pyenv', 'prefix', 'venv-run-testsuite'):
                return real_subprocess_run(
                    ('echo', 'pyenv/path/somewhere'), **kwargs)
            if args[0] == ('asdf', 'where', 'python', '3.10.4'):
                return real_subprocess_run(
                    ('echo', 'asdf/path/somewhere'), **kwargs)
            return real_subprocess_run(*args, **kwargs)

        with patch.object(platform, "system", return_value='Linux'), \
             patch.object(subprocess, "run", mock_run):
            venvs = venvrun.guess()
            self.assertTrue(venvs[0], "subscriptability")
            self.assertListEqual(
                sorted(venvs),
                sorted(
                    os.path.normpath(os.path.join(os.getcwd(), x))
                    for x in (
                            'venv', '.venv', os.curdir,
                            '.direnv/python-3.10.4',
                            '.direnv/virtualenv',
                            'pyenv/path/somewhere',
                            'asdf/path/somewhere'
                    ))
            )

    def testGuessDedupe(self) -> None:

        def mock_run(*args: Any, **kwargs: Any) -> CompletedProcess[str]:
            if args[0] == ('pyenv', 'prefix', 'venv-run-testsuite'):
                return real_subprocess_run(
                    ('echo', 'venv'), **kwargs)
            return real_subprocess_run(*args, **kwargs)

        with patch.object(platform, "system", return_value='Linux'), \
             patch.object(subprocess, "run", mock_run):
            venvs = venvrun.guess()
            self.assertTrue(venvs[0], "subscriptability")
            self.assertListEqual(
                sorted(venvs),
                sorted(
                    os.path.normpath(os.path.join(os.getcwd(), x))
                    for x in (
                            'venv', '.venv', os.curdir,
                            '.direnv/python-3.10.4',
                            '.direnv/virtualenv',
                    ))
            )

    def testGuessDedupeSymlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="venv-run") as tempdir:
            symlink = os.path.join(tempdir, "venv")
            os.symlink(os.path.join(os.getcwd(), "venv"), symlink)

            def mock_run(*args: Any, **kwargs: Any) -> CompletedProcess[str]:
                if args[0] == ('pyenv', 'prefix', 'venv-run-testsuite'):
                    return real_subprocess_run(
                        ('echo', symlink), **kwargs)
                return real_subprocess_run(*args, **kwargs)

            with patch.object(platform, "system", return_value='Linux'), \
                 patch.object(subprocess, "run", mock_run):
                venvs = venvrun.guess()
                self.assertTrue(venvs[0], "subscriptability")
                self.assertListEqual(
                    sorted(venvs),
                    sorted(
                        os.path.normpath(os.path.join(os.getcwd(), x))
                        for x in (
                                'venv', '.venv', os.curdir,
                                '.direnv/python-3.10.4',
                                '.direnv/virtualenv',
                        ))
                )
