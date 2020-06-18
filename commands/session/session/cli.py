#!/usr/bin/env python3
from argparse import ArgumentParser
from . import client, server
import base64
import sys


def debug(s):
    if True:
        if isinstance(s, str):
            print(s)
        else:
            print((s()))


def parse_and_run():
    parser = ArgumentParser(description="Execute Markdown Code Blocks")
    subparsers = parser.add_subparsers()

    server_parser = subparsers.add_parser(
        "server", help="Start the server. It may be helpful to run in under (z)daemon.",
    )
    server_parser.add_argument("verb", choices=["start"], nargs=1)
    server_parser.set_defaults(func=run_server)

    client_parser = subparsers.add_parser("client")
    client_parser.add_argument(
        "verb", choices=["start", "execute", "stop", "kill"], nargs=1
    )
    client_parser.add_argument("filename")
    client_parser.set_defaults(func=run_client)
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(e)
        return False


def run_server(args):
    server.app.run(port=9009, threaded=True)


def run_client(args):
    session = base64.urlsafe_b64encode(args.filename)
    rs = client.RemoteSession(session, "localhost", 9009)
    verb = args.verb[0]
    if verb == "execute":
        lines = sys.stdin.readlines()
        lines = [l.rstrip("\n") for l in lines]
        output = rs.execute(lines, auto_start=True)
        output = [o + "\n" for o in output]
        sys.stdout.writelines(output)
    else:
        if not getattr(rs, verb)():
            raise ValueError("Error: %s did not succeed." % args.verb)
