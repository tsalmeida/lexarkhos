from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import poetry_typing


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "poetry_typing.py", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def test_default_behavior_emits_one_line_per_prompt() -> None:
    result = run_cli("--seed", "123", "--count", "2", "verses.txt")
    stdout = result.stdout
    assert stdout.endswith("\n")
    lines = stdout.rstrip("\n").split("\n")
    assert len(lines) == 2


def test_single_line_contains_only_final_newline() -> None:
    result = run_cli("--seed", "123", "--count", "5", "--single-line", "verses.txt")
    stdout = result.stdout
    assert stdout.endswith("\n")
    assert stdout.count("\n") == 1


def test_single_line_matches_expected_prompts() -> None:
    result = run_cli("--seed", "123", "--count", "5", "--single-line", "verses.txt")
    expected = (
        "Sing in me, Muse, and through me tell the story of that man. 1857 ]$ "
        "Nel mezzo del cammin di nostra vita mi ritrovai per una selva oscura. 7672 ]% "
        "A seagull soars in the pink evening, tracing wind with patient wings. 1625 ,: "
        "On the mountains of the moon, down the valley of the shadow. 6583 @( "
        "O mar salgado, quanto do teu sal / São lágrimas de Portugal! 3212 :+\n"
    )
    assert result.stdout == expected


def test_blank_lines_are_skipped_in_single_line_mode(tmp_path: Path) -> None:
    verses_file = tmp_path / "verses.txt"
    verses_file.write_text(
        "First light on quiet seas.\n\nSecond verse appearing.\n   \nThird stanza stays.\n",
        encoding="utf-8",
    )

    result = run_cli("--seed", "99", "--single-line", str(verses_file))

    random.seed(99)
    prompts = [
        poetry_typing.generate_prompt(verse)
        for verse in poetry_typing.iter_verses(verses_file)
    ]
    expected_output = " ".join(prompts) + ("\n" if prompts else "")
    assert result.stdout == expected_output
