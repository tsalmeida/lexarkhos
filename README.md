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
   ```

Each emitted line will contain the verse, a four-digit number between 1000 and
9999, and two symbols selected from the set shown below:

```
~`!@#$%^&*()-_=+[]{};:'",.<>/?\|
```

Use the `--count` option to limit the number of verses printed, or `--seed` to
reproduce an earlier run.

The generated output can be copied into the typing practice tool of your
choice.
