#!/usr/bin/env python

import argparse
import sys
import urllib.request

__version__ = "0.1.1"


def check_health(url, quiet):
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"

    try:
        urllib.request.urlopen(url)
    except Exception as e:
        if not quiet:
            try:
                error = e.reason.strerror
            except AttributeError:
                error = str(e)
            print(f"Error: {error}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Health check a URL and exit with code 1 on HTTP errors."
    )
    parser.add_argument("url", type=str, help="URL to check")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress error messages"
    )

    args = parser.parse_args()

    check_health(args.url, args.quiet)


if __name__ == "__main__":
    main()
