from typing import Sequence

import os
import argparse

from ..config import Config
from ..utils.io import FileResource, StdinResource
from ..utils.logger import getLogger
from ..utils.importlib import silent_import
from ..core.api import FormatCode

from ._base import BaseAdapter

logger = getLogger(__name__)


def _build_argument_parser():
    parser = argparse.ArgumentParser(description='Default formatter for lambdex')
    diff_inplace_quiet_group = parser.add_mutually_exclusive_group()
    diff_inplace_quiet_group.add_argument(
        '-d',
        '--diff',
        action='store_true',
        help='print the diff for the fixed source',
    )
    diff_inplace_quiet_group.add_argument(
        '-i',
        '--in-place',
        action='store_true',
        help='make changes to files in place',
    )
    diff_inplace_quiet_group.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='output nothing and set return value',
    )

    parser.add_argument(
        '-p',
        '--parallel',
        action='store_true',
        help='run in parallel when formatting multiple files.',
    )

    parser.add_argument('files', nargs='*', help='reads from stdin when no files are specified.')
    return parser


class DummyAdapter(BaseAdapter):
    def _make_config(self) -> Config:
        parser = _build_argument_parser()

        bopts = parser.parse_args(self.backend_argv)

        if (bopts.in_place or bopts.diff) and not bopts.files:
            logger.error('cannot use --in-place or --diff flags when reading from stdin')

        cfg = Config(adapter='yapf')
        cfg.in_place = bopts.in_place
        cfg.parallel = bopts.parallel
        cfg.print_diff = bopts.diff
        cfg.quiet = bopts.quiet
        cfg.files = bopts.files

        return cfg

    def _job(self, filename=None) -> bool:
        if filename is None:
            resource = StdinResource(self.config)
        else:
            resource = FileResource(self.config, filename)

        resource.set_backend_output(resource.source)

        formatted_code = FormatCode(resource.backend_output_stream.readline)
        resource.write_formatted_code(formatted_code)

        return resource.is_changed(formatted_code)

    def _get_backend_cmd_for_resource(self, resource) -> Sequence[str]:
        pass