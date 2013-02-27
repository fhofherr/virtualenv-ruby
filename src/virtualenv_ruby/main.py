# coding=utf-8

import sys
from virtualenv_ruby import errors


def main(environment):
    if 'VIRTUAL_ENV' not in environment:
        sys.exit(errors.ExitCodes.NO_VIRTUAL_ENV)
