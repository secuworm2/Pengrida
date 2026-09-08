import re
import sys

REPLACEMENTS = [
    (b"FRIDA", b"PENGU"),
    (b"Frida", b"Pengu"),
    (b"frida", b"pengu"),
]

# Matches runs of 4+ printable ASCII bytes (what `strings` would report),
# so replacement only ever happens inside identified string data, never
# inside code or arbitrary binary structures.
STRING_RUN = re.compile(rb"[\x20-\x7e]{4,}")


def scrub(data: bytes) -> tuple[bytes, int]:
    count = 0
    out = bytearray(data)

    for match in STRING_RUN.finditer(data):
        start, end = match.span()
        chunk = data[start:end]
        new_chunk = chunk
        for old, new in REPLACEMENTS:
            n = new_chunk.count(old)
            if n:
                count += n
                new_chunk = new_chunk.replace(old, new)
        if new_chunk != chunk:
            assert len(new_chunk) == len(chunk), "length mismatch, aborting"
            out[start:end] = new_chunk

    return bytes(out), count


def main(argv):
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <binary>", file=sys.stderr)
        return 2

    path = argv[1]
    with open(path, "rb") as f:
        data = f.read()

    patched, count = scrub(data)

    if len(patched) != len(data):
        print("FATAL: output size changed, refusing to write", file=sys.stderr)
        return 1

    with open(path, "wb") as f:
        f.write(patched)

    print(f"[*] {path}: replaced {count} occurrence(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
