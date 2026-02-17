import os
import time
from pathlib import Path
from typing import Optional, TextIO


def _open_file_safely(path: Path) -> Optional[TextIO]:
    try:
        return path.open("r", encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None


def _get_inode(path: Path) -> Optional[int]:
    try:
        return path.stat().st_ino
    except FileNotFoundError:
        return None


def tail_file(
    file_path: Path,
    follow: bool = True,
    sleep_interval_seconds: float = 0.5,
) -> None:
    """
    Tail a log file and optionally follow for new lines.

    If the file does not exist yet, this function will wait for it to appear.
    If the file is rotated or truncated, it will re-open and continue following.
    """
    file_path = Path(file_path)

    current_file: Optional[TextIO] = None
    current_inode: Optional[int] = None

    try:
        while True:
            if current_file is None:
                current_file = _open_file_safely(file_path)
                current_inode = _get_inode(file_path)
                if current_file is None:
                    # Wait for the file to be created
                    time.sleep(sleep_interval_seconds)
                    continue
                # Seek to end initially (tail -f behavior)
                current_file.seek(0, os.SEEK_END)

            # Read any new lines available
            line = current_file.readline()
            if line:
                print(line, end="")
            else:
                if not follow:
                    break
                # Detect log rotation or truncation
                new_inode = _get_inode(file_path)
                if new_inode is None or (current_inode is not None and new_inode != current_inode):
                    try:
                        if current_file is not None:
                            current_file.close()
                    finally:
                        current_file = None
                        current_inode = None
                        continue

                time.sleep(sleep_interval_seconds)
    except KeyboardInterrupt:
        pass
    finally:
        if current_file is not None:
            try:
                current_file.close()
            except Exception:
                pass


