#!/usr/bin/env python3
"""news-23 b124 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error:", msg, file=sys.stderr)
    return 1


def validate_png(data):
    """Validate the source PNG header and chunk structure (manual parse, no PIL)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 33:
        return "file too short for IHDR"
    # first chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8, colour type 2 or 6
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        return "first chunk is not a 13-byte IHDR"
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return f"wrong dimensions {w}x{h}, expected 1024x1024"
    if depth != 8 or ctype_b not in (2, 6):
        return f"unsupported IHDR (bit depth {depth}, colour type {ctype_b})"
    if comp != 0 or filt != 0 or inter != 0:
        return "unsupported IHDR compression/filter/interlace"
    crc_stored = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != crc_stored:
        return "IHDR CRC mismatch"
    # walk the remaining chunks: CRC each, IDAT non-empty, IEND last with no trailing data.
    # Layout: 8-byte signature + 25-byte IHDR chunk (4 len + 4 type + 13 data + 4 CRC),
    # so the next chunk starts at byte 33, not 37.
    pos = 33
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        cname = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return f"truncated chunk {cname.decode('latin1')}"
        chunk_crc = zlib.crc32(cname + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if chunk_crc != crc_stored:
            return f"CRC mismatch in chunk {cname.decode('latin1')}"
        if cname == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if cname == b"IEND":
            if clen != 0:
                return "IEND chunk must be 0 bytes"
            if pos + 12 != len(data):
                return "trailing data after IEND"
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload too small"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if os.path.isfile(outdir_abs):
        return fail(f"MAKEFUN_OUTPUT_DIR is a file: {outdir}")
    # refuse to write inside the repo (grader runs from a read-only copy)
    if os.path.commonpath([outdir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the source repo")
    if not os.path.isfile(src):
        return fail(f"source not found: {src}")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail(f"source too small: {len(data)} bytes")
    if len(data) > MAX_BYTES:
        return fail(f"source too large: {len(data)} bytes (max {MAX_BYTES})")
    err = validate_png(data)
    if err:
        return fail(err)
    os.makedirs(outdir_abs, exist_ok=True)
    dst = os.path.join(outdir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output does not match source byte-for-byte")
    print(f"wrote {dst} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
