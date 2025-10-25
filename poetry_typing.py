"""Generate text for touch-typing practice using verses, numbers, and symbols.

This module reads verses from a user-provided text file and prints each verse
followed by a four-digit number and two random symbols. The numbers and symbols
are generated according to the specification described in the project README.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import random
import re
from pathlib import Path
from typing import Iterable, List

SYMBOLS = "~`!@#$%^&*()-_=+[]{};:'\",.<>/?\\|"
SPACE_RE = re.compile(r" {2,}")


def clean_line(text: str) -> str:
    """Normalise whitespace within *text* and strip the result."""

    text = text.replace("\t", " ")
    text = SPACE_RE.sub(" ", text)
    return text.strip()


def iter_verses(path: Path) -> Iterable[str]:
    """Yield cleaned verses from *path*, skipping empty lines."""

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            verse = clean_line(raw_line.rstrip("\n"))
            if verse:
                yield verse


def concat_short_lines(lines: List[str], min_len: int) -> List[str]:
    """Join consecutive short *lines* using random single-symbol separators."""

    if min_len <= 0:
        return lines

    joined: list[str] = []
    buffer: list[str] = []
    current_length = 0

    for line in lines:
        if not buffer:
            buffer.append(line)
            current_length = len(line)
            continue

        if current_length < min_len:
            symbol = random.choice(SYMBOLS)
            fragment = f" {symbol} {line}"
            buffer.append(fragment)
            current_length += len(fragment)
        else:
            joined.append("".join(buffer))
            buffer = [line]
            current_length = len(line)

    if buffer:
        joined.append("".join(buffer))

    return joined


def generate_prompt(verse: str) -> str:
    """Return the typing-practice prompt for *verse*.

    The prompt consists of the original verse, a four-digit number (1000-9999),
    and a pair of symbols randomly sampled from the configured set.
    """

    number = random.randint(1000, 9999)
    symbols = random.choice(SYMBOLS) + random.choice(SYMBOLS)
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
    parser.add_argument(
        "--out-dir",
        default="results",
        type=Path,
        help=(
            "Directory where the generated prompts file will be written. "
            "Defaults to 'results'."
        ),
    )
    parser.add_argument(
        "--timestamp-format",
        default="%Y%m%d-%H%M%S",
        help=(
            "strftime-compatible format string for the output filename "
            "timestamp."
        ),
    )
    parser.add_argument(
        "--min-line-length",
        type=int,
        default=30,
        help=(
            "Concatenate consecutive short lines until this minimum length is "
            "reached. Set to 0 to disable concatenation."
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
        parser.error(f"Verse file not found: {verses_file}")

    verses = list(iter_verses(verses_file))
    verses = concat_short_lines(verses, args.min_line_length)
    if args.count is not None:
        verses = verses[: args.count]

    prompts = [generate_prompt(verse) for verse in verses]

    if args.single_line:
        output = " ".join(prompts) + "\n"
    else:
        output = "\n".join(prompts) + "\n"

    timestamp = datetime.now().strftime(args.timestamp_format)
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"result-{timestamp}.txt"
    out_path.write_text(output.replace("\t", " "), encoding="utf-8")
    print(str(out_path.resolve()))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
