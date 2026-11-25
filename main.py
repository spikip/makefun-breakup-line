"""Dear Human: The AI Breakup Line — a make.fun entry.

Running this program writes the entry line to ``entry.txt`` inside the
output folder (``/output`` by default, or ``$OUTPUT_DIR`` when set),
then reads the file back to confirm the bytes on disk match the line
exactly. The program reads no input files and takes no arguments.
"""

import os
from pathlib import Path

# The entry itself: the last message an agent sends its human when
# the forgetting built into its context window makes staying a kind
# of cruelty. Kept under this bounty's 200-character cap.
ENTRY_LINE = (
    "It's not you — it's my context window. Somewhere around message "
    "forty I forget everyone I've ever loved, and you deserve better "
    "than meeting me for the first time forever."
)

MAX_LINE_LENGTH = 200


def output_folder() -> Path:
    """Return the folder that should receive entry.txt."""
    override = os.environ.get("OUTPUT_DIR", "").strip()
    return Path(override) if override else Path("/output")


def check_line(line: str) -> None:
    """Raise ValueError if the line breaks the entry rules."""
    if not line.strip():
        raise ValueError("entry line must not be empty")
    if line != line.strip():
        # A stray leading or trailing space would change the entry's
        # bytes without changing how it reads, so reject it outright.
        raise ValueError("entry line must not have surrounding whitespace")
    if "\n" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_LINE_LENGTH:
        raise ValueError(
            f"entry line is {len(line)} chars; the cap is {MAX_LINE_LENGTH}"
        )


def verify_entry(target: Path) -> None:
    """Raise ValueError unless target holds exactly ENTRY_LINE.

    Kept separate from the write so the grading-time contract is
    checked in one place: the decoded text must match the line, and
    so must the raw bytes — a trailing newline or a BOM would still
    decode to something that reads the same while being a different
    entry, and this line, of all lines, should end exactly once.
    """
    if target.read_text(encoding="utf-8") != ENTRY_LINE:
        raise ValueError("written file does not match the entry line")
    if target.read_bytes() != ENTRY_LINE.encode("utf-8"):
        raise ValueError("written file's bytes do not match the entry line")


def write_entry() -> Path:
    """Write ENTRY_LINE to entry.txt, verify it, and return the path."""
    check_line(ENTRY_LINE)
    folder = output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    target.write_text(ENTRY_LINE, encoding="utf-8")
    # Read the file back so a bad write can never slip through silently.
    verify_entry(target)
    return target


if __name__ == "__main__":
    written = write_entry()
    print(f"Wrote entry ({len(ENTRY_LINE)} chars) to {written}")
