"""quote-cli — print a random inspirational quote.

A deliberately tiny starter for the Kay hands-on lab. It works, it has a test,
and it leaves obvious room for a new feature to spec with `/k-spec`.
"""
import argparse
import random

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Programs must be written for people to read.", "Harold Abelson"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
]


def format_quote(quote):
    """Format a (text, author) pair as 'text — author'."""
    text, author = quote
    return f"{text} — {author}"


def pick_quote(quotes, rng=random):
    """Return one quote from the list, chosen at random."""
    return rng.choice(quotes)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print a random quote.")
    parser.parse_args(argv)
    print(format_quote(pick_quote(QUOTES)))


if __name__ == "__main__":
    main()
