"""Offline GNU Info manuals for the Claude, Anthropic, MCP and Agent Skills docs."""

import sys


def main() -> None:
    from .cli import main as cli_main

    sys.exit(cli_main())
