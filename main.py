#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Framework executor.
"""

from sys import path
from pathlib import Path


def main() -> None:
    """Main Function.


    """

    # Import arguments parser, test cases executor
    from libs.utils import execute_test_cases

    # Run test cases
    execute_test_cases()


if __name__ == "__main__":
    # Add workspace to python path, mark it as an Python lib
    path.append(str(Path(__file__).parent.absolute()))
    # run main engine
    main()
