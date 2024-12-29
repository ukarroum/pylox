import argparse
from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

had_error = False

def run_script(script: Path):
    with script.open() as f:
        run(f.read())
    if had_error:
        sys.exit(65)

def run_prompt():
    global had_error

    while True:
        code = input(">>> ")
        if not code:
            break
        run(code)
        had_error = False

def run(code: str):
    pass

def report(line: int, msg: str, where: str = ""):
    global had_error

    logger.error(f"[{line}][{where}] Error: {msg}")
    had_error = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PyLox, a python implementation of the lox language")

    parser.add_argument("script", help="The script to be executed")

    args = parser.parse_args()

    if args.script:
        run_script(Path(args.script))
    else:
        run_prompt()
