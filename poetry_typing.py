"""Generate text for touch-typing practice using verses, numbers, and symbols.

This module reads verses from a user-provided text file and prints each verse
followed by a four-digit number and two random symbols. The numbers and symbols
are generated according to the specification described in the project README.
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Iterable

SYMBOLS = "~`!@#$%^&*()-_=+[]{};:'\",.<>/?\\|"


def iter_verses(path: Path) -> Iterable[str]:
    """Yield verses from *path*, skipping empty lines.

    Lines are yielded in the exact order they appear in the file. Empty lines
    are ignored to avoid emitting blank practice prompts that contain only the
    number and symbol block.
    """

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            verse = line.rstrip("\n")
            if verse.strip():
                yield verse


def generate_prompt(verse: str) -> str:
    """Return the typing-practice prompt for *verse*.

    The prompt consists of the original verse, a four-digit number (1000-9999),
    and a pair of symbols randomly sampled from the configured set.
    """

    number = random.randint(1000, 9999)
    symbols = "".join(random.sample(SYMBOLS, 2))
    return f"{verse} {number} {symbols}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate text for touch-typing practice using verses from a file."
        )
    )
    parser.add_argument(
        "verses_file",
        nargs="?",
        default="verses.txt",
        type=Path,
        help=(
            "Path to the text file containing one verse per line. Defaults to "
            "'verses.txt' in the current directory."
        ),
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help=(
            "Number of verses to emit. By default, all non-empty lines in the "
            "file are used."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help=(
            "Optional random seed for reproducible number and symbol blocks."
        ),
    )
    parser.add_argument(
        "--single-line",
        action="store_true",
        help=(
            "Emit all generated prompts on a single line separated by spaces."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    verses_file: Path = args.verses_file
    if not verses_file.exists():
        raise SystemExit(f"Verse file not found: {verses_file}")

    verses = list(iter_verses(verses_file))
    if args.count is not None:
        verses = verses[: args.count]

    prompts = [generate_prompt(verse) for verse in verses]

    if args.single_line:
        if prompts:
            print(" ".join(prompts))
    else:
        for prompt in prompts:
            print(prompt)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
