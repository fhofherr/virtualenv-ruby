# coding=utf-8

import os
import sys
from virtualenv_ruby import errors
from virtualenv_ruby import hooks


def modify_and_write_hooks(hook_builder):
    hook_builder.add_environment_variable(
        'GEM_HOME', '$VIRTUAL_ENV/lib/ruby/gems')
    hook_builder.add_environment_variable(
        'GEM_PATH', '""')
    hook_builder.extend_path('$GEM_HOME/bin')
    hook_builder.write_hooks()


def main(environment=os.environ):
    if 'VIRTUAL_ENV' not in environment:
        sys.exit(errors.ExitCodes.NO_VIRTUAL_ENV)
    hook_builder = hooks.HookBuilder(environment['VIRTUAL_ENV'])
    modify_and_write_hooks(hook_builder)
