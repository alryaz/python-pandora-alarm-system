"""Command-line client for Pandora CAS Python API."""
import argparse
import logging
import sys
from os import getenv
from typing import Final

import aiohttp

_LOGGER: Final = logging.getLogger(__name__)

from pandora_alarm_system import PandoraOnlineAccount, CommandID

try:
    # Python >= 3.11
    from enum import StrEnum
except ImportError:
    # Python < 3.11
    from strenum import StrEnum


class OutputFormat(StrEnum):
    READABLE = "readable"
    JSON = "json"
    CSV = "csv"
    XML = "xml"
    VALUE = "value"
    YAML = "yaml"


async def list_devices(api: PandoraOnlineAccount, fmt: str):
    await api.async_refresh_devices()

    return {
        device_id: device.name for device_id, device in api.devices.items()
    }


async def process_argparse_args(args: argparse.Namespace) -> None:
    async with aiohttp.ClientSession() as session:
        try:
            api = PandoraOnlineAccount(
                session, args.username, args.password, logger=_LOGGER
            )
            await api.async_authenticate()
        except BaseException as e:
            print(f"Error: {e}", file=sys.stderr)
            return
        try:
            command_id = CommandID[args.action.upper()]
        except (KeyError, AttributeError):
            pass
        else:
            await api.async_remote_command(args.device, command_id)
            return
        if args.action == "list":
            print(await list_devices(api, args.format))


def main(*args):
    logging.basicConfig(level=logging.DEBUG)
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv()

    # Load parameters from environment
    username = getenv("PANDORA_USERNAME", None)
    password = getenv("PANDORA_PASSWORD", None)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--username",
        required=not username,
        default=username,
        type=str,
        help="username to log into pandora",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=not password,
        default=password,
        type=str,
        help="password to log into pandora",
    )
    parser.add_argument(
        "-f",
        "--format",
        default=OutputFormat.READABLE,
        type=str,
        choices=[e for e in OutputFormat],
        help="specify output format (if applicable)",
    )

    action = parser.add_subparsers(dest="action", required=True)
    action.add_parser("list")

    subparser = action.add_parser("command")
    subparser.add_argument(
        "id", required=True, type=int, help="command identifier"
    )

    for command in CommandID:
        subparser = action.add_parser(command.name.lower())
        subparser.add_argument(
            "-d",
            "--device",
            required=True,
            type=int,
            help="unique device identifier",
        )

    import asyncio

    asyncio.run(process_argparse_args(parser.parse_args(args or None)))
