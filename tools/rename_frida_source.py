import re
import sys
from pathlib import Path

REPLACEMENTS = [
    ("FRIDA", "PENGU"),
    ("Frida", "Pengu"),
    ("frida", "pengu"),
]

# Only real source files get text-substituted. meson.build / meson_options.txt /
# .wrap files are deliberately excluded: they reference subproject and
# dependency names (e.g. subproject('frida-gum'), dependency('frida-gum-1.0'))
# that must keep matching the actual on-disk directory names, which this
# script does NOT rename. Renaming those identifiers without also renaming
# directories would break meson's subproject resolution.
SOURCE_SUFFIXES = {".vala", ".c", ".h", ".cpp", ".cc", ".hpp", ".m", ".mm", ".java"}
EXTRA_EXACT_NAMES = {"Makefile"}

EXCLUDE_DIR_NAMES = {".git", "releng", "deps", "build", "toolchain"}


def should_process(path: Path) -> bool:
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return False
    if path.suffix in SOURCE_SUFFIXES:
        return True
    if path.name in EXTRA_EXACT_NAMES:
        return True
    return False


def rename_java_package_dir(core_root: Path):
    old_dir = core_root / "src" / "android-helper" / "re" / "frida"
    new_dir = core_root / "src" / "android-helper" / "re" / "pengu"
    if old_dir.is_dir():
        new_dir.parent.mkdir(parents=True, exist_ok=True)
        old_dir.rename(new_dir)
        print(f"[*] moved {old_dir} -> {new_dir}")
    else:
        print(f"[*] no android-helper java package dir at {old_dir}, skipping move")


def rename_text_in_tree(root: Path) -> int:
    total = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if not should_process(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text = text
        for old, new in REPLACEMENTS:
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            n = sum(text.count(old) for old, _ in REPLACEMENTS)
            total += n
            print(f"[*] {path}: {n} replacement(s)")
    return total


def main(argv):
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <frida-core-dir>", file=sys.stderr)
        return 2

    core_root = Path(argv[1])
    if not core_root.is_dir():
        print(f"{core_root}: not a directory", file=sys.stderr)
        return 1

    rename_java_package_dir(core_root)
    total = rename_text_in_tree(core_root)
    print(f"[*] total replacements: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
