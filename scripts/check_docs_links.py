#!/usr/bin/env python3
"""
Check internal links in Markdown files.
- Verifies relative .md links exist
- Verifies anchor links (#section) exist in target file
- Skips external HTTP(S) links (optional: could add HEAD check)
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
MD_FILES = list(ROOT.rglob("*.md")) + list(DOCS_DIR.rglob("*.md")) if DOCS_DIR.exists() else list(ROOT.rglob("*.md"))

# Regex for markdown links: [text](url)
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Track errors
errors = []

def resolve_link(source_file: Path, link: str) -> tuple[bool, str]:
    """Return (ok, error_message)."""
    parsed = urlparse(link)
    if parsed.scheme in ('http', 'https', 'mailto', 'tel'):
        return True, ""  # skip external
    if link.startswith('#'):
        # Anchor in same file
        return True, ""  # anchor existence checked separately
    # Relative path
    target = (source_file.parent / link).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return False, f"link escapes repo root: {link}"
    if not target.exists():
        # Try adding .md if missing
        if not target.suffix and target.with_suffix('.md').exists():
            return True, ""
        return False, f"target not found: {target.relative_to(ROOT)}"
    if target.is_dir():
        # Directory index
        index = target / "README.md"
        if not index.exists():
            return False, f"directory has no README.md: {target.relative_to(ROOT)}"
    return True, ""

def check_anchors(source_file: Path, link: str) -> bool:
    """Verify anchor exists in target file."""
    if '#' not in link:
        return True
    base, anchor = link.split('#', 1)
    anchor = anchor.lower().replace(' ', '-').replace('.', '').replace(',', '')
    if not base:
        target = source_file
    else:
        target_path = (source_file.parent / base).resolve()
        try:
            target_path.relative_to(ROOT)
        except ValueError:
            return True
        if not target_path.exists():
            if target_path.with_suffix('.md').exists():
                target_path = target_path.with_suffix('.md')
            else:
                return True  # will be caught by link existence check
        target = target_path
    try:
        content = target.read_text(encoding='utf-8')
    except Exception:
        return True
    # Find headings
    for line in content.splitlines():
        line_stripped = line.lstrip()
        if line_stripped.startswith('#'):
            heading_text = re.sub(r'^#+\s*', '', line_stripped).strip()
            heading_id = heading_text.lower().replace(' ', '-').replace('.', '').replace(',', '')
            if heading_id == anchor:
                return True
    return False

def main():
    print(f"Checking {len(MD_FILES)} Markdown files...")
    for md_file in MD_FILES:
        if md_file.name == 'CHANGELOG.md':
            # Skip changelog (many version links)
            continue
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"{md_file}: read error: {e}")
            continue

        for match in LINK_RE.finditer(content):
            link = match.group(2).strip()
            ok, msg = resolve_link(md_file, link)
            if not ok:
                errors.append(f"{md_file.relative_to(ROOT)}: {msg} (link: {link})")
            elif link.startswith('#') or ('#' in link and not link.startswith('http')):
                # Check anchor
                if not check_anchors(md_file, link):
                    errors.append(f"{md_file.relative_to(ROOT)}: anchor not found: {link}")

    if errors:
        print("\n❌ Link errors found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ All internal links OK")

if __name__ == "__main__":
    main()