# Copyright the author(s) of intc.
#
# This source code is licensed under the Apache license found in the
# LICENSE file in the root directory of this source tree.

"""Intc Language Server command line interface."""

import argparse
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from textwrap import dedent

from platformdirs import user_log_dir

from intc_lsp.server import intc_server
from intc_lsp.version import __version__

log_dir = user_log_dir("intc_lsp")


def get_version() -> str:
    """Get the program version."""
    return __version__


def cli() -> None:
    """intc language server cli entrypoint."""
    parser = argparse.ArgumentParser(
        prog="intc-language-server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="intc language server: an LSP wrapper for intc.",
        epilog=dedent(
            """\
            Examples:

                Run over stdio     : intc-language-server
                Run over tcp       : intc-language-server --tcp
                Run over websockets:
                    # only need to pip install once per env
                    pip install pygls[ws]
                    intc-language-server --ws

            Notes:

                For use with web sockets, user must first run
                'pip install pygls[ws]' to install the correct
                version of the websockets library.
            """
        ),
    )
    parser.add_argument(
        "--version",
        help="display version information and exit",
        action="store_true",
    )
    parser.add_argument(
        "--tcp",
        help="use TCP web server instead of stdio",
        action="store_true",
    )
    parser.add_argument(
        "--ws",
        help="use web socket server instead of stdio",
        action="store_true",
    )
    parser.add_argument(
        "--host",
        help="host for web server (default 127.0.0.1)",
        type=str,
        default="127.0.0.1",
    )
    parser.add_argument(
        "--port",
        help="port for web server (default 9999)",
        type=int,
        default=9999,
    )
    parser.add_argument(
        "--log-file",
        default=os.path.join(log_dir, "log"),
        help="redirect logs to file specified",
        type=str,
    )
    parser.add_argument(
        "--log_level",
        default=2,
    )
    args = parser.parse_args()
    if args.version:
        print(get_version())
        sys.exit(0)
    if args.tcp and args.ws:
        print(
            "Error: --tcp and --ws cannot both be specified",
            file=sys.stderr,
        )
        sys.exit(1)
    log_level = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(
        args.log_level,
        logging.WARN,
    )
    logger = logging.getLogger()
    logger_intc = logging.getLogger("intc_lsp")

    if args.log_file:
        if not os.path.isfile(os.path.dirname(args.log_file)):
            os.makedirs(os.path.dirname(args.log_file), exist_ok=True)
            logger.setLevel(log_level)
            logger_intc.setLevel(log_level)
            file_handler = RotatingFileHandler(
                filename=args.log_file,
                mode="w",
                encoding="utf8",
                maxBytes=5 * 1024 * 1024,
            )
            file_formatter = logging.Formatter(
                fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                datefmt="%m/%d/%Y %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
    else:
        logging.basicConfig(stream=sys.stderr, level=log_level)

    if args.tcp:
        intc_server.start_tcp(host=args.host, port=args.port)
    elif args.ws:
        intc_server.start_ws(host=args.host, port=args.port)
    else:
        intc_server.start_io()


if __name__ == "__main__":
    cli()
