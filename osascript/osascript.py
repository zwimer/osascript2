from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import cast
import subprocess

__all__ = ("run", "run_bytes")


def _sub_run(path: str | Path, text: bool) -> tuple[int, str, str] | tuple[int, bytes, bytes]:
    p = subprocess.run(["osascript", path], text=text, capture_output=True, check=False)
    return p.returncode, p.stdout, p.stderr


def _run(cmd: str | Path, text: bool) -> tuple[int, str, str] | tuple[int, bytes, bytes]:
    if isinstance(cmd, Path):
        return _sub_run(cmd, text)
    with NamedTemporaryFile("w", delete_on_close=False) as f:
        f.write(cmd)
        f.close()
        return _sub_run(f.name, text)


def run(cmd: str | Path) -> tuple[int, str, str]:
    """Execute the given applescript command or file (run with subprocess' text=True)

    Args:
        cmd: The string command (or path to the applescript file) to execute

    Returns:
        A tuple containing: (return code, stdout, and stderr)
    """
    return cast(tuple[int, str, str], _run(cmd, True))


def run_bytes(cmd: str | Path) -> tuple[int, bytes, bytes]:
    """Execute the given applescript command or file (run with subprocess' text=False)

    Args:
        cmd: The string command (or path to the applescript file) to execute

    Returns:
        A tuple containing: (return code, stdout, and stderr)
    """
    return cast(tuple[int, bytes, bytes], _run(cmd, False))
