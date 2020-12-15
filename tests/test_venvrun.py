import os
import sys
import unittest
from subprocess import run as real_subprocess_run
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'src'))
import venvrun


class VenvRunTest(unittest.TestCase):

    def setUp(self):
        self.oldcwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(__file__), 'fixture'))

    def tearDown(self):
        os.chdir(self.oldcwd)

    def testGuess(self):

        def mock_run(*args, **kwargs):
            if args[0] == ('pyenv', 'prefix', 'venv-run-testsuite'):
                return real_subprocess_run(
                    ('echo', 'pyenv/path/somewhere'), **kwargs)
            return real_subprocess_run(*args, **kwargs)

        with patch.object(venvrun.platform, "system", return_value='Linux'), \
             patch.object(venvrun.subprocess, "run", mock_run):
            venvs = venvrun.guess()
            self.assertListEqual(sorted(venvs), sorted([
                'venv', '.venv', os.curdir, 'pyenv/path/somewhere'
            ]))
