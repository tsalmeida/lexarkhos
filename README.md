# lexarkhos

Generates text for touch-typing practice.

## Usage

1. Place your verses in `verses.txt`, one verse per line. Blank lines are
   ignored. The default file provided here demonstrates the expected format and
   supports UTF-8 text, so you can safely include accents and punctuation.
2. Run the generator:

   ```bash
   python poetry_typing.py            # reads from verses.txt by default
   python poetry_typing.py my_poem.txt  # use a different verse file
   python poetry_typing.py --single-line verses.txt  # emit a single joined line
   ```

Each emitted line will contain the verse, a four-digit number between 1000 and
9999, and two symbols selected from the set shown below. By default the script
prints one prompt per line; pass `--single-line` to emit all prompts on a single
line separated by spaces.

```
~`!@#$%^&*()-_=+[]{};:'",.<>/?\|
```

Use the `--count` option to limit the number of verses printed, `--seed` to
reproduce an earlier run, or `--single-line` to concatenate all prompts into one
continuous line with a trailing newline.

The generated output can be copied into the typing practice tool of your
choice.
