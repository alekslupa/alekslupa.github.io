#!/usr/bin/env python3
"""
Generate repository statistics CSVs for the ePortfolio meta page.

Run this from the repo root once before rendering the ePortfolio page:

    python3 scripts/generate_repo_stats.py

Outputs four CSV files into the data/ directory:

  data/commits_over_time.csv     - daily commit count
  data/file_inventory.csv        - file count and size by extension
  data/scss_growth.csv           - SCSS line count at each scss-touching commit
  data/top_edited_files.csv      - files ranked by edit frequency

Re-run whenever you want the ePortfolio meta page to reflect the latest repo state.
"""

import csv
import os
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


def run_git(args):
    """Run a git command from the repo root and return stdout as a string."""
    result = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def commits_over_time():
    """Daily commit count. Each row: date, commits."""
    log = run_git(["log", "--pretty=format:%cs"])
    counts = Counter(line.strip() for line in log.splitlines() if line.strip())
    rows = sorted(counts.items())

    with open(DATA_DIR / "commits_over_time.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "commits"])
        for date, n in rows:
            writer.writerow([date, n])

    print(f"  commits_over_time.csv: {len(rows)} dates, {sum(counts.values())} total commits")


def file_inventory():
    """Current file count and total size by extension."""
    counts = Counter()
    sizes = Counter()
    skip_dirs = {".git", "node_modules", "_freeze", ".quarto", "docs"}

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for filename in files:
            ext = Path(filename).suffix.lower() or "(no extension)"
            full = Path(root) / filename
            try:
                size = full.stat().st_size
            except OSError:
                size = 0
            counts[ext] += 1
            sizes[ext] += size

    rows = sorted(counts.items(), key=lambda kv: -kv[1])

    with open(DATA_DIR / "file_inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["extension", "count", "total_bytes"])
        for ext, n in rows:
            writer.writerow([ext, n, sizes[ext]])

    print(f"  file_inventory.csv: {len(rows)} extensions, {sum(counts.values())} files")


def scss_growth():
    """
    Line count of styles.scss after each commit that touched it.

    Walks the commit history and uses `git show` to fetch the contents of
    styles.scss at each touching commit, then counts non-blank lines.
    """
    log = run_git([
        "log",
        "--pretty=format:%H|%cs",
        "--follow",
        "--",
        "styles.scss",
    ])

    rows = []
    for line in log.splitlines():
        if not line.strip():
            continue
        sha, date = line.split("|", 1)
        try:
            content = run_git(["show", f"{sha}:styles.scss"])
        except subprocess.CalledProcessError:
            continue
        line_count = sum(1 for ln in content.splitlines() if ln.strip())
        rows.append((date, sha[:8], line_count))

    rows.reverse()

    with open(DATA_DIR / "scss_growth.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "commit", "lines"])
        for row in rows:
            writer.writerow(row)

    if rows:
        print(f"  scss_growth.csv: {len(rows)} touching commits, "
              f"{rows[0][2]} -> {rows[-1][2]} lines")
    else:
        print("  scss_growth.csv: no commits found that touched styles.scss")


def top_edited_files(limit=15):
    """Files ranked by number of commits that touched them."""
    log = run_git(["log", "--pretty=format:", "--name-only"])
    files = Counter()
    skip_prefixes = ("docs/", "_freeze/", ".quarto/", "node_modules/")

    for line in log.splitlines():
        path = line.strip()
        if not path:
            continue
        if any(path.startswith(p) for p in skip_prefixes):
            continue
        files[path] += 1

    rows = files.most_common(limit)

    with open(DATA_DIR / "top_edited_files.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "edits"])
        for path, n in rows:
            writer.writerow([path, n])

    print(f"  top_edited_files.csv: top {len(rows)} of {len(files)} tracked files")


if __name__ == "__main__":
    print(f"Generating repo stats from {REPO_ROOT}")
    print(f"Writing to {DATA_DIR}")
    print()
    commits_over_time()
    file_inventory()
    scss_growth()
    top_edited_files()
    print()
    print("Done. Four CSVs written to data/.")
