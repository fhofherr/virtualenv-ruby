# coding=utf-8

from os.path import join
from unittest import TestCase
from mock import mock_open, patch

from virtualenv_ruby import hooks


class TestHookBuilder(TestCase):

    def setUp(self):
        self.virtual_env_dir = '/path/to/some/dir'
        self.postactivate_hook_file = join(
            self.virtual_env_dir, 'bin', 'postactivate')
        self.postdeactivate_hook_file = join(
            self.virtual_env_dir, 'bin', 'postdeactivate')
        self.hook_builder = hooks.HookBuilder(self.virtual_env_dir)
        self.mock_open = mock_open()

    def test_extends_path_in_postactivate_hook(self):
        path_ext = '$GEM_HOME/bin'
        self.hook_builder.extend_path(path_ext)
        expected_lines = [
            '{path_backup}=$PATH\n'.format(
                path_backup=hooks._VIRTUALENV_RUBY_OLD_PATH),
            'export PATH="{path_ext}:$PATH"\n'.format(path_ext=path_ext),
        ]
        with self.patched_open():
            self.hook_builder.write_postactivate_hook()
        self.assert_appends_to_hook(
            self.postactivate_hook_file, expected_lines)

    def test_resets_path_in_postdeactivate_hook(self):
        expected_lines = [
            'export PATH=${path_backup}\n'.format(
                path_backup=hooks._VIRTUALENV_RUBY_OLD_PATH),
            'unset {path_backup}\n'.format(
                path_backup=hooks._VIRTUALENV_RUBY_OLD_PATH),
        ]
        self.hook_builder.extend_path('$GEM_HOME/bin')
        with self.patched_open():
            self.hook_builder.write_postdeactivate_hook()
        self.assert_appends_to_hook(
            self.postdeactivate_hook_file, expected_lines)

    def test_appends_environment_variable_to_postactivate_hook(self):
        var_name = 'GEM_HOME'
        var_value = '$VIRTUAL_ENV/lib/ruby/gems'
        expected_lines = ['export ' + var_name + "=" + var_value + '\n']

        self.hook_builder.add_environment_variable(var_name, var_value)
        with self.patched_open():
            self.hook_builder.write_postactivate_hook()
        self.assert_appends_to_hook(
            self.postactivate_hook_file, expected_lines)

    def test_appends_environment_variable_to_postdeactivate_hook(self):
        var_name = 'GEM_HOME'
        var_value = '$VIRTUAL_ENV/lib/ruby/gems'
        expected_lines = ['unset ' + var_name + '\n']

        self.hook_builder.add_environment_variable(var_name, var_value)
        with self.patched_open():
            self.hook_builder.write_postdeactivate_hook()
        self.assert_appends_to_hook(
            self.postdeactivate_hook_file, expected_lines)

    def test_adds_environment_variables_before_changing_path(self):
        self.hook_builder.add_environment_variable('some_var', 'some_value')
        self.hook_builder.extend_path('some_ext')
        expected_lines = (
            self.hook_builder._create_postactivate_env_var_lines()
            + self.hook_builder._create_postactivate_path_ext_lines())
        with self.patched_open():
            self.hook_builder.write_postactivate_hook()
        self.assert_appends_to_hook(
            self.postactivate_hook_file, expected_lines)

    def assert_appends_to_hook(self, hook_file, expected_lines):
        self.mock_open.assert_called_once_with(hook_file, 'a')
        handle = self.mock_open()
        handle.writelines.assert_called_once_with(expected_lines)

    def patched_open(self):
        return patch('__builtin__.open', self.mock_open, create=True)
