#!/usr/bin/env python3
"""Sync doppler-dsp/.github's profile README from doppler's README.md.

The org profile page can't use doppler's relative markdown links (they
resolve relative to docs/index.md in the rendered docs site, not to
README.md's own location at the repo root) or the bare LICENSE badge
link (GitHub profile READMEs don't get repo-relative link resolution
the way a repo's own README does) -- both need rewriting to absolute
https://github.com/doppler-dsp/doppler/blob/main/... links.

Run on a schedule (see sync-readme.yml) rather than a push trigger:
README.md lives in a different repo, so there's no push event here to
react to, and polling avoids needing a cross-repo write token (the
workflow's own GITHUB_TOKEN only needs write access to THIS repo).
"""

import re
import sys
import urllib.request

SOURCE_URL = (
    "https://raw.githubusercontent.com/doppler-dsp/doppler/main/README.md"
)
DEST_PATH = "profile/README.md"

# Both LICENSE and every relative .md link are already written relative to
# the REPO ROOT in README.md, so they only need the host prefix -- no path
# is added. Links appear both as markdown `](target)` and raw HTML
# `href="target"` (the badge anchors), so each rewrite covers both syntaxes.
#
# This used to insert `docs/`, from when README.md was a byte-identical twin
# of docs/index.md and its links were docs-relative. doppler now GENERATES
# README.md from docs/index.md's readme-sync region (scripts/gen_readme.py),
# rewriting the links to repo-root form on the way -- so the compensation
# became a double prefix and every navigation link on the org profile 404'd
# as `docs/docs/...`. Measured 2026-08-22: 12 of 12 relative links were dead.
# If README.md ever goes back to docs-relative links, fix it THERE; a second
# opinion about paths in this script is what broke it the first time.
_LICENSE_RE = re.compile(r'(\]\(|href=")LICENSE(\)|")')
_RELATIVE_MD_RE = re.compile(r'(\]\(|href=")([a-zA-Z][^)"\s]*\.md)(\)|")')
_BASE = "https://github.com/doppler-dsp/doppler/blob/main"


def rewrite_links(text: str) -> str:
    text = _LICENSE_RE.sub(rf"\1{_BASE}/LICENSE\2", text)
    text = _RELATIVE_MD_RE.sub(rf"\1{_BASE}/\2\3", text)
    return text


def main() -> int:
    with urllib.request.urlopen(SOURCE_URL, timeout=30) as resp:
        source = resp.read().decode("utf-8")

    synced = rewrite_links(source)

    try:
        with open(DEST_PATH, encoding="utf-8") as f:
            current = f.read()
    except FileNotFoundError:
        current = None

    if synced == current:
        print("profile README already in sync; nothing to do")
        return 0

    with open(DEST_PATH, "w", encoding="utf-8") as f:
        f.write(synced)
    print(f"synced {DEST_PATH} from {SOURCE_URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
