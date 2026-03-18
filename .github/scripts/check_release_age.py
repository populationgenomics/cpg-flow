"""Check the release age of packages proposed in a Dependabot PR."""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone


def get_pypi_release_date(package: str, version: str) -> datetime | None:
    """Get the release date of a package version from PyPI."""
    try:
        url = f'https://pypi.org/pypi/{package}/{version}/json'
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        upload_time = data.get('urls', [{}])[0].get('upload_time_iso_8601')
        if upload_time:
            return datetime.fromisoformat(upload_time.replace('Z', '+00:00'))
        return None
    except Exception as e:
        print(f'Error fetching {package} {version}: {e}', file=sys.stderr)
        return None


def parse_pr_body(body: str) -> list[dict[str, str]]:
    """Parse Dependabot PR body to extract package updates.

    Looks for lines like: "Bumps `package` from 1.0.0 to 2.0.0"
    """
    updates = []
    for line in body.splitlines():
        line = line.strip()
        if 'from' not in line.lower() or 'to' not in line.lower():
            continue
        parts = line.split()
        try:
            from_idx = next(i for i, w in enumerate(parts) if w.lower() == 'from')
            to_idx = next(i for i, w in enumerate(parts) if w.lower() == 'to')
            updates.append(
                {
                    'package': parts[from_idx - 1].strip('`').strip(','),
                    'old_version': parts[from_idx + 1].strip(','),
                    'new_version': parts[to_idx + 1].strip(','),
                }
            )
        except (StopIteration, IndexError):
            continue
    return updates


def format_age(days: int) -> str:
    if days == 0:
        return 'Released today 🆕'
    if days == 1:
        return 'Released yesterday ⚠️'
    indicator = '⚠️' if days < 7 else '✅'
    return f'Released {days} days ago {indicator}'


def main() -> None:
    pr_body = os.getenv('PR_BODY', '')
    if not pr_body:
        print('Missing PR_BODY environment variable', file=sys.stderr)
        sys.exit(1)

    updates = parse_pr_body(pr_body)
    if not updates:
        sys.exit(0)

    lines = ['## 📦 Dependency Release Age', '']
    now = datetime.now(timezone.utc)
    for update in updates:
        release_date = get_pypi_release_date(update['package'], update['new_version'])
        lines.append(f'- **{update["package"]}**: `{update["old_version"]}` → `{update["new_version"]}`')
        if release_date:
            days = (now - release_date).days
            lines.append(f'  - {format_age(days)}')
        else:
            lines.append('  - Release date unavailable ❓')

    lines.extend(['', '---', '⚠️ = Released within the last week | ✅ = Released more than a week ago'])
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
