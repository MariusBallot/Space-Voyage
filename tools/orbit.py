"""Ring spacing helpers for Space-Voyage."""


def ring_gap(speed, base=40):
    """Distance between two consecutive rings at a given ship speed: faster ships need more room."""
    return base + speed * 2
