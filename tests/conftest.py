import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--record",
        action="store_true",
        default=False,
        help='Record new cassettes?')



