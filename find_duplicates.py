#!/usr/bin/env python3
"""
Duplicate file finder using MD5 hashing.
Groups:
  1. True duplicates    - same MD5 hash (identical content, any filename)
  2. Name collisions    - same filename but different MD5 hash
"""

import os
import hashlib
import argparse
from collections import defaultdict
from datetime import datetime


def md5_of_file(path, chunk_size=65536):
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError) as e:
        return None, str(e)


def scan_directory(root):
    by_hash = defaultdict(list)   # hash -> [paths]
    by_name = defaultdict(list)   # filename -> [(path, hash)]
    errors = []
    total = 0

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            total += 1
            result = md5_of_file(full_path)
            if isinstance(result, tuple):
                errors.append((full_path, result[1]))
                continue
            file_hash = result
            by_hash[file_hash].append(full_path)
            by_name[filename].append((full_path, file_hash))

    return by_hash, by_name, errors, total


def build_report(root, by_hash, by_name, errors, total):
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("=" * 72)
    lines.append(f"  DUPLICATE FILE REPORT")
    lines.append(f"  Scanned : {root}")
    lines.append(f"  Date    : {now}")
    lines.append(f"  Files   : {total}")
    lines.append("=" * 72)

    # ── Section 1: True duplicates (same hash, any name) ──────────────────
    true_dupes = {h: paths for h, paths in by_hash.items() if len(paths) > 1}
    lines.append(f"\n{'─'*72}")
    lines.append(f"  SECTION 1 — True Duplicates (identical content)")
    lines.append(f"  Groups : {len(true_dupes)}")
    lines.append(f"{'─'*72}")

    if true_dupes:
        for i, (h, paths) in enumerate(sorted(true_dupes.items()), 1):
            try:
                size = os.path.getsize(paths[0])
                size_str = _human_size(size)
                wasted = _human_size(size * (len(paths) - 1))
            except OSError:
                size_str = wasted = "?"
            lines.append(f"\n  [{i}] MD5: {h}  |  Size: {size_str}  |  Copies: {len(paths)}  |  Wasted: {wasted}")
            for p in sorted(paths):
                lines.append(f"        {p}")
    else:
        lines.append("\n  None found.")

    # ── Section 2: Same name, different content ────────────────────────────
    name_conflicts = {
        name: entries
        for name, entries in by_name.items()
        if len(entries) > 1 and len({h for _, h in entries}) > 1
    }
    lines.append(f"\n{'─'*72}")
    lines.append(f"  SECTION 2 — Same Filename, Different Content")
    lines.append(f"  Groups : {len(name_conflicts)}")
    lines.append(f"{'─'*72}")

    if name_conflicts:
        for i, (name, entries) in enumerate(sorted(name_conflicts.items()), 1):
            lines.append(f"\n  [{i}] Filename: {name}  |  Variants: {len(entries)}")
            for path, h in sorted(entries):
                try:
                    size_str = _human_size(os.path.getsize(path))
                except OSError:
                    size_str = "?"
                lines.append(f"        MD5: {h}  Size: {size_str}")
                lines.append(f"        Path: {path}")
    else:
        lines.append("\n  None found.")

    # ── Errors ─────────────────────────────────────────────────────────────
    if errors:
        lines.append(f"\n{'─'*72}")
        lines.append(f"  ERRORS ({len(errors)} files could not be read)")
        lines.append(f"{'─'*72}")
        for path, msg in errors:
            lines.append(f"  {path}")
            lines.append(f"    -> {msg}")

    lines.append(f"\n{'='*72}")
    return "\n".join(lines)


def _human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def main():
    parser = argparse.ArgumentParser(description="Find duplicate files by MD5 hash.")
    parser.add_argument("directory", help='Root directory to scan (e.g. "G:\\My Drive")')
    parser.add_argument("-o", "--output", help="Write report to this file instead of stdout")
    args = parser.parse_args()

    root = os.path.abspath(args.directory)
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a valid directory.")
        raise SystemExit(1)

    print(f"Scanning {root} ...")
    by_hash, by_name, errors, total = scan_directory(root)
    report = build_report(root, by_hash, by_name, errors, total)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
