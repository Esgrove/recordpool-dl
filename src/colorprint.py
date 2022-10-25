"""
Color print helper
Akseli Lukkarila
2019 - 2022
"""

import sys

import colorama

colorama.init(strip=False, convert=False)


class Color:
    """Interface for Colorama colors."""

    red = colorama.Fore.RED
    green = colorama.Fore.GREEN
    yellow = colorama.Fore.YELLOW
    blue = colorama.Fore.BLUE
    magenta = colorama.Fore.MAGENTA
    cyan = colorama.Fore.CYAN
    white = colorama.Fore.WHITE


def get_color(text: str, color=Color.white, bold=False) -> str:
    """Format string with color using Colorama."""
    return f"{colorama.Style.BRIGHT if bold else ''}{color}{text}{colorama.Style.RESET_ALL}"


def print_bold(text: str, color=Color.white, **kwargs):
    """Print bold text."""
    print(get_color(text, color, True), **kwargs)


def print_color(text: str, color=Color.white, bold=False, **kwargs):
    """
    Print text with color using Colorama.

    You can pass optional extra arguments for the Python default print function if wanted:

    - sep='separator': Specify how to separate the objects, if there is more than one. Default is ' '
    - end='end': Specify what to print at the end. Default is '\\n' (line feed)
    - file: An object with a write method. Default is sys.stdout
    - flush: A Boolean, specifying if the output is flushed (True) or buffered (False). Default is False
    """
    print(get_color(text, color, bold), **kwargs)


def print_error_and_exit(text: str, exit_code=1):
    """Print error message and exit with given exit code."""
    print_error(text)
    sys.exit(exit_code)


def print_error(text: str, bold=False, **kwargs):
    print_color(f"ERROR: {text}", Color.red, bold, **kwargs)


def print_warn(text: str, bold=False, **kwargs):
    print_color(f"WARNING: {text}", Color.yellow, bold, **kwargs)


def print_green(text: str, bold=False, **kwargs):
    print_color(text, Color.green, bold, **kwargs)


def print_yellow(text: str, bold=False, **kwargs):
    print_color(text, Color.yellow, bold, **kwargs)


def print_red(text: str, bold=False, **kwargs):
    print_color(text, Color.red, bold, **kwargs)


def print_blue(text: str, bold=False, **kwargs):
    print_color(text, Color.red, bold, **kwargs)


def print_magenta(text: str, bold=False, **kwargs):
    print_color(text, Color.magenta, bold, **kwargs)


def print_cyan(text: str, bold=False, **kwargs):
    print_color(text, Color.cyan, bold, **kwargs)
