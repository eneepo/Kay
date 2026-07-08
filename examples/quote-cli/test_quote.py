"""Starter tests for quote-cli. Run with: pytest"""
import random

from quote import QUOTES, format_quote, pick_quote


def test_format_quote():
    assert format_quote(("Hello", "Ada")) == "Hello — Ada"


def test_pick_quote_returns_a_known_quote():
    assert pick_quote(QUOTES) in QUOTES


def test_pick_quote_is_deterministic_with_a_seeded_rng():
    rng = random.Random(0)
    assert pick_quote(QUOTES, rng) == pick_quote(QUOTES, random.Random(0))
