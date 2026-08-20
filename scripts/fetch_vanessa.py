"""Backward-compatible wrapper: fetch Vanessa via fetch_heroes. """

from __future__ import annotations

import sys

from fetch_heroes import fetch_hero, get_hero


def main() -> None:
    count = fetch_hero(get_hero("vanessa"))
    print(f"Fetched {count} Vanessa cards.")


if __name__ == "__main__":
    main()
