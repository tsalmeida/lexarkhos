from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from poetry_typing import SYMBOLS


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "poetry_typing.py", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def test_writes_timestamped_file_and_contents_single_line(tmp_path: Path) -> None:
    result = run_cli(
        "--seed",
        "123",
        "--count",
        "5",
        "--single-line",
        "--out-dir",
        str(tmp_path),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    assert output_path.parent == tmp_path
    assert output_path.exists()

    contents = output_path.read_text(encoding="utf-8")
    expected = (
        "Sing in me, Muse, and through me tell the story of that man. 1857 ]$ "
        "Nel mezzo del cammin di nostra vita mi ritrovai per una selva oscura. 7672 ]% "
        "A seagull soars in the pink evening, tracing wind with patient wings. 1625 ,: "
        "On the mountains of the moon, down the valley of the shadow. 6583 @( "
        "O mar salgado, quanto do teu sal / São lágrimas de Portugal! 3212 ::\n"
    )
    assert result.stdout == f"{output_path.resolve()}\n"
    assert contents == expected


def test_writes_one_prompt_per_line_default_mode(tmp_path: Path) -> None:
    result = run_cli(
        "--seed",
        "123",
        "--count",
        "2",
        "--out-dir",
        str(tmp_path),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    contents = output_path.read_text(encoding="utf-8")
    assert contents.endswith("\n")
    lines = contents.rstrip("\n").split("\n")
    assert len(lines) == 2
    for line in lines:
        assert line


def test_creates_out_dir_if_missing(tmp_path: Path) -> None:
    out_dir = tmp_path / "nested" / "results"
    assert not out_dir.exists()

    result = run_cli("--seed", "7", "--count", "1", "--out-dir", str(out_dir))

    output_path = Path(result.stdout.rstrip("\n"))
    assert out_dir.exists()
    assert out_dir.is_dir()
    assert output_path.parent == out_dir
    assert output_path.exists()


def test_skips_blank_lines(tmp_path: Path) -> None:
    verses_file = tmp_path / "verses.txt"
    verses_file.write_text(
        "First light on quiet seas.\n\n   \nSecond verse appearing.\nThird stanza stays.\n",
        encoding="utf-8",
    )

    result = run_cli("--seed", "99", "--out-dir", str(tmp_path), str(verses_file))

    output_path = Path(result.stdout.rstrip("\n"))
    contents = output_path.read_text(encoding="utf-8")
    lines = contents.rstrip("\n").split("\n")
    assert lines and all(line.strip() for line in lines)
    assert len(lines) == 2


def test_tabs_and_spaces_normalized(tmp_path: Path) -> None:
    verses = tmp_path / "verses.txt"
    verses.write_text("abhorred\tthraldom        [note]\n", encoding="utf-8")

    result = run_cli(
        "--seed",
        "1",
        "--count",
        "1",
        "--out-dir",
        str(tmp_path),
        str(verses),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    line = output_path.read_text(encoding="utf-8").strip()
    assert "\t" not in line
    assert "  " not in line
    assert "abhorred thraldom [note]" in line


def test_trailing_pair_always_two_symbols(tmp_path: Path) -> None:
    verses = tmp_path / "verses.txt"
    verses.write_text("alpha\n", encoding="utf-8")

    result = run_cli(
        "--seed",
        "2",
        "--count",
        "5",
        "--out-dir",
        str(tmp_path),
        str(verses),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    lines = output_path.read_text(encoding="utf-8").strip().split("\n")
    for line in lines:
        parts = line.rsplit(" ", 2)
        assert len(parts) == 3
        number, symbols = parts[1:]
        assert number.isdigit() and len(number) == 4
        assert len(symbols) == 2
        assert all(ch in SYMBOLS for ch in symbols)


def test_concatenates_short_lines_with_single_symbol_joiners(tmp_path: Path) -> None:
    verses = tmp_path / "verses.txt"
    verses.write_text(
        "abiding romance\nabject submission\nabjured ambition\n",
        encoding="utf-8",
    )

    result = run_cli(
        "--seed",
        "123",
        "--out-dir",
        str(tmp_path),
        "--min-line-length",
        "30",
        str(verses),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    line = output_path.read_text(encoding="utf-8").strip()
    body = line.rsplit(" ", 2)[0]
    joiners = [f" {symbol} " for symbol in SYMBOLS]
    assert any(joiner in body for joiner in joiners)
    assert "  " not in body


def test_disable_concatenation(tmp_path: Path) -> None:
    verses = tmp_path / "verses.txt"
    verses.write_text("short one\nshort two\n", encoding="utf-8")

    result = run_cli(
        "--seed",
        "1",
        "--out-dir",
        str(tmp_path),
        "--min-line-length",
        "0",
        str(verses),
    )

    output_path = Path(result.stdout.rstrip("\n"))
    lines = output_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
