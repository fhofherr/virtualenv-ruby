# coding=utf-8

from unittest import TestCase
from virtualenv_ruby import main
from virtualenv_ruby import errors


class TestMain(TestCase):

    def test_fails_if_not_in_virtual_env(self):
        environment = {}
        with self.assertRaises(SystemExit) as e:
            main.main(environment)
        self.assertEqual(errors.ExitCodes.NO_VIRTUAL_ENV, e.exception.code)
