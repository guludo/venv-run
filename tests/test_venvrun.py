import os
import sys
import unittest
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
        with patch("venvrun.platform.system", return_value='Linux'):
            venvs = venvrun.guess()
            self.assertListEqual(sorted(venvs), sorted(['venv']))
