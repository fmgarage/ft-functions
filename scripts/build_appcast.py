#!/usr/bin/env python3
"""
Build functions.json (appcast) from all functions/**/*.fmfn.

Reads the header comment of each custom function, extracts name, version
history, params and about, and verifies that the version code returned by
"--version" matches the latest @version entry.

Usage:
    scripts/build_appcast.py [--out site/functions.json] [--strict]

Environment (set by GitHub Actions, optional locally):
    GITHUB_SHA      commit used for the pinned raw link
    SITE_URL        base url of the Pages site (default from mkdocs.yml)
    REPO_URL        github repo url (default from mkdocs.yml)
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUNCTIONS_DIR = ROOT / "functions"

RE_NAME = re.compile(r"^/\*\s*([A-Za-z_][\w.]*)\s*\((.*?)\)", re.S)
RE_ABOUT = re.compile(r"@about\s+(.+)")
RE_VERSION_LINE = re.compile(
    r"^\s*(?:@version\s+)?(\d+)\.(\d+)\.(\d+)(?:-\d+)?\s*[-–]\s*(\d{2})\.(\d{2})\.(\d{4})",
    re.M,
)
RE_VERSION_CODE = re.compile(r'--version"[^;]*;\s*(\d{7,9})\s*;')
RE_CALL = re.compile(r"\b([A-Z][A-Za-z0-9]*\.[a-z][A-Za-z0-9]*_v\d+)\s*\(")


def read_mkdocs_defaults():
    site_url, repo_url = "", ""
    cfg = ROOT / "mkdocs.yml"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            if line.startswith("site_url:"):
                site_url = line.split(":", 1)[1].strip()
            elif line.startswith("repo_url:"):
                repo_url = line.split(":", 1)[1].strip()
    return site_url.rstrip("/"), repo_url.rstrip("/")


def parse_function(path: Path, site_url: str, repo_url: str, sha: str, problems: list):
    text = path.read_text(encoding="utf-8")
    header_end = text.find("*/")
    header = text[:header_end] if header_end > 0 else text
    body = text[header_end:] if header_end > 0 else ""

    file_name = path.stem  # Namespace.function_vN
    rel = path.relative_to(FUNCTIONS_DIR).as_posix()

    m = RE_NAME.search(header)
    header_name = m.group(1) if m else ""
    params = [p.strip() for p in m.group(2).split(";") if p.strip()] if m else []
    if header_name and header_name != file_name:
        problems.append(f"{rel}: header name '{header_name}' != file name '{file_name}'")

    about = RE_ABOUT.search(header)
    about = about.group(1).strip() if about else ""

    versions = []
    for v in RE_VERSION_LINE.finditer(header):
        major, minor, patch, dd, mm, yyyy = map(int, v.groups())
        versions.append(((major, minor, patch), f"{yyyy:04d}-{mm:02d}-{dd:02d}"))
    if not versions:
        problems.append(f"{rel}: no @version history found")
        latest, date = (0, 0, 0), ""
    else:
        latest, date = max(versions, key=lambda x: x[0])

    version_code = latest[0] * 1_000_000 + latest[1] * 1_000 + latest[2]
    semver = ".".join(map(str, latest))

    code_match = RE_VERSION_CODE.search(body)
    if not code_match:
        problems.append(f"{rel}: no --version command found")
    else:
        code_in_body = int(code_match.group(1))
        if code_in_body != version_code:
            problems.append(
                f"{rel}: --version returns {code_in_body}, header says {version_code} ({semver})"
            )

    major_in_name = re.search(r"_v(\d+)$", file_name)
    if not major_in_name:
        problems.append(f"{rel}: file name has no _vN suffix")
    elif int(major_in_name.group(1)) != latest[0]:
        problems.append(f"{rel}: name says v{major_in_name.group(1)}, header says {semver}")

    requires = sorted({c for c in RE_CALL.findall(body) if c != file_name})

    namespace, _, short = file_name.partition(".")
    entry = {
        "name": file_name,
        "version": version_code,
        "semver": semver,
        "date": date,
        "about": about,
        "params": params,
        "requires": requires,
        "url": f"{site_url}/{rel}",
        "docs": f"{site_url}/{path.parent.relative_to(FUNCTIONS_DIR).as_posix()}/",
        "source": f"{repo_url.replace('github.com', 'raw.githubusercontent.com')}/{sha}/functions/{rel}",
        "sha256": hashlib.sha256(text.encode('utf-8')).hexdigest(),
        "bytes": len(text.encode("utf-8")),
    }
    return namespace, short, entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="site/functions.json")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any problem")
    args = ap.parse_args()

    site_url, repo_url = read_mkdocs_defaults()
    site_url = os.environ.get("SITE_URL", site_url).rstrip("/")
    repo_url = os.environ.get("REPO_URL", repo_url).rstrip("/")
    sha = os.environ.get("GITHUB_SHA", "main")

    problems = []
    functions = {}
    for path in sorted(FUNCTIONS_DIR.rglob("*.fmfn")):
        if "_archive" in path.parts:
            continue
        namespace, short, entry = parse_function(path, site_url, repo_url, sha, problems)
        functions.setdefault(namespace, {})[short] = entry

    appcast = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": sha,
        "count": sum(len(v) for v in functions.values()),
        "functions": functions,
    }

    out = Path(args.out) if Path(args.out).is_absolute() else ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(appcast, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} with {appcast['count']} functions")

    for p in problems:
        print(f"WARNING: {p}", file=sys.stderr)
    if problems and args.strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
