from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess

__all__ = ("run",)


def _run(path: str | Path) -> tuple[int, bytes, bytes]:
    p = subprocess.run(["osascript", path], capture_output=True, check=False)
    return p.returncode, p.stdout, p.stderr


def run(cmd: str | Path) -> tuple[int, bytes, bytes]:
    """
    Execute the given applescript command or file
    Return the (return code, stdout, and stderr)
    """
    if isinstance(cmd, Path):
        return _run(cmd)
    with NamedTemporaryFile("w", delete_on_close=False) as f:
        f.write(cmd)
        f.close()
        return _run(f.name)
