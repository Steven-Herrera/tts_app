"""Utility helpers."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="Text-to-Speech CLI")

    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to input .txt file",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to output .wav file",
    )

    parser.add_argument(
        "--config",
        required=False,
        type=Path,
        default=Path("configs/default.yaml"),
        help="Path to YAML config file",
    )

    return parser.parse_args()
