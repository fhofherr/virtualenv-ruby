# coding=utf-8

from os.path import join

_VIRTUALENV_RUBY_OLD_PATH = '_VIRTUALENV_RUBY_OLD_PATH'


class HookBuilder(object):
    def __init__(self, virtualenv_dir):
        self.virtualenv_dir = virtualenv_dir
        self._environment_vars = {}
        self._path_extensions = []

    def add_environment_variable(self, var_name, var_value):
        self._environment_vars[var_name] = var_value

    def extend_path(self, path_ext):
        self._path_extensions.append(path_ext)

    def write_hooks(self):
        self.write_postactivate_hook()
        self.write_postdeactivate_hook()

    def write_postactivate_hook(self):
        postactivate_hook_file = self.__get_hook_file('postactivate')
        env_vars = self._create_postactivate_env_var_lines()
        path_exts = self._create_postactivate_path_ext_lines()
        self.__write_hook_file(postactivate_hook_file, env_vars + path_exts)

    def _create_postactivate_env_var_lines(self):
        line_tmpl = 'export {var_name}={var_value}'
        return [
            line_tmpl.format(var_name=n, var_value=v)
            for n, v in self._environment_vars.items()]

    def _create_postactivate_path_ext_lines(self):
        if not self._path_extensions:
            return []
        path_backup = '{path_backup}=$PATH'.format(
            path_backup=_VIRTUALENV_RUBY_OLD_PATH)
        path_exts = 'export PATH="{paths}:$PATH"'.format(
            paths=''.join(self._path_extensions))
        return [path_backup, path_exts]

    def write_postdeactivate_hook(self):
        postdeactivate_hook_file = self.__get_hook_file('postdeactivate')
        env_vars = self._create_postdeactivate_env_var_lines()
        path_mod = self._create_postdeactivate_path_lines()
        self.__write_hook_file(postdeactivate_hook_file, env_vars + path_mod)

    def _create_postdeactivate_env_var_lines(self):
        line_tmpl = 'unset {var_name}'
        return [line_tmpl.format(var_name=n) for n in self._environment_vars]

    def _create_postdeactivate_path_lines(self):
        if not self._path_extensions:
            return []
        return [
            'export PATH=${path_backup}'.format(
                path_backup=_VIRTUALENV_RUBY_OLD_PATH),
            'unset {path_backup}'.format(
                path_backup=_VIRTUALENV_RUBY_OLD_PATH),
        ]

    def __get_hook_file(self, hook_name):
        return join(self.virtualenv_dir, 'bin', hook_name)

    def __write_hook_file(self, hook_file, lines):
        with open(hook_file, 'a') as file:
            file.writelines(lines)
