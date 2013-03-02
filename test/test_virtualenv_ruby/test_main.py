# coding=utf-8

from mock import call, MagicMock
from unittest import TestCase
from virtualenv_ruby import main
from virtualenv_ruby import errors
from virtualenv_ruby import hooks


class TestMain(TestCase):

    def test_fails_if_not_in_virtual_env(self):
        environment = {}
        with self.assertRaises(SystemExit) as e:
            main.main(environment)
        self.assertEqual(errors.ExitCodes.NO_VIRTUAL_ENV, e.exception.code)


class TestModifyHooks(TestCase):

    def setUp(self):
        self.mock_hook_builder = MagicMock(spec=hooks.HookBuilder)

    def test_modifies_and_writes_hooks(self):
        expected_calls = [
            call.add_environment_variable(
                'GEM_HOME', '$VIRTUAL_ENV/lib/ruby/gems'),
            call.add_environment_variable('GEM_PATH', '""'),
            call.extend_path('$GEM_HOME/bin'),
            call.write_hooks()
        ]
        main.modify_and_write_hooks(self.mock_hook_builder)
        self.assertEqual(expected_calls, self.mock_hook_builder.method_calls)
