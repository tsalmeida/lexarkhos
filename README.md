# lexarkhos

Generates text for touch-typing practice.

## Usage

1. Place your verses in `verses.txt`, one verse per line. Blank lines are
   ignored. Each verse is cleaned automatically: tabs become single spaces,
   multiple spaces collapse to one, and leading/trailing whitespace is removed.
   The default file provided here demonstrates the expected format and
   supports UTF-8 text, so you can safely include accents and punctuation.
2. Run the generator:

   ```bash
   python poetry_typing.py                # writes results/result-YYYYMMDD-HHMMSS.txt
   python poetry_typing.py my_poem.txt    # custom verses file
   python poetry_typing.py --single-line  # one joined line
   python poetry_typing.py --out-dir out              # custom output directory
   python poetry_typing.py --min-line-length 20       # join short lines sooner
   python poetry_typing.py --min-line-length 0        # disable joining entirely
   ```

Each run produces a timestamped text file containing the generated prompts. The
script prints the absolute path of that file to standard output.

Each emitted line will contain the cleaned verse text, a four-digit number
between 1000 and 9999, and **exactly two** symbols selected (with replacement)
from the set shown below. By default the script writes one prompt per line;
pass `--single-line` to emit all prompts on a single line separated by spaces.

Short verses are concatenated before the number/symbol block is appended. When
enabled (the default threshold is 30 characters), consecutive short lines are
combined until they reach the threshold, with a single random symbol surrounded
by spaces joining each fragment. Set `--min-line-length 0` to disable this
behaviour.

```
~`!@#$%^&*()-_=+[]{};:'",.<>/?\|
```

Use the `--count` option to limit the number of verses printed, `--seed` to
reproduce an earlier run, or `--single-line` to concatenate all prompts into one
continuous line with a trailing newline.

The generated output can be copied into the typing practice tool of your
choice.
