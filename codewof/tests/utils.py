"""Utility functions for testing."""

import random


def random_boolean(percent=50):
    """Return a random boolean.

    Args:
        Percentage (int): Chance the value is True.

    Returns:
        Random boolean value.
    """
    return random.randrange(100) < percent
