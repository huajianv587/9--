#!/usr/bin/env python3
"""Check current Safari / Capital IQ status without modifying web data."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads"


APPLESCRIPT = r'''
tell application "Safari"
    set wcount to count of windows
    set out to "window_count=" & wcount
    if wcount > 0 then
        set t to current tab of front window
        set out to out & linefeed & "title=" & name of t
        set out to out & linefeed & "url=" & URL of t
        try
            set jsResult to do JavaScript "document.title + '\n' + location.href + '\n' + (document.body ? document.body.innerText.slice(0,1000) : '')" in t
            set out to out & linefeed & "js_status=ok" & linefeed & jsResult
        on error errMsg number errNum
            set out to out & linefeed & "js_status=error " & errNum & ": " & errMsg
        end try
    end if
    return out
end tell
'''


SYSTEM_EVENTS_SCRIPT = r'''
tell application "System Events"
    tell process "Safari"
        set out to "frontmost=" & frontmost
        try
            set out to out & linefeed & "window_count=" & (count of windows)
            repeat with w in windows
                set out to out & linefeed & "window=" & name of w & " pos=" & (position of w as text) & " size=" & (size of w as text)
            end repeat
        on error errMsg number errNum
            set out to out & linefeed & "ax_error=" & errNum & ": " & errMsg
        end try
    end tell
    return out
end tell
'''


def run_osascript(script: str, timeout: int = 20) -> dict[str, object]:
    proc = subprocess.run(
        ["osascript"],
        input=script,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def parse_lines(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            parsed[key.strip()] = value.strip()
    return parsed


def recent_downloads(after: datetime) -> list[dict[str, object]]:
    patterns = ["SPGlobal_Export*.xlsx", "*Capital*.xlsx", "*.csv", "*.xlsx"]
    seen: set[Path] = set()
    rows = []
    for pattern in patterns:
        for path in DOWNLOADS.glob(pattern):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            stat = path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            if modified > after:
                rows.append(
                    {
                        "path": str(path),
                        "size": stat.st_size,
                        "mtime": modified.isoformat(timespec="seconds"),
                    }
                )
    return sorted(rows, key=lambda row: str(row["mtime"]), reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--after", required=True, help="local timestamp, e.g. '2026-06-01 18:54:00'")
    parser.add_argument("--out-json", default="", help="optional JSON output path")
    args = parser.parse_args()

    after = datetime.strptime(args.after, "%Y-%m-%d %H:%M:%S")
    safari = run_osascript(APPLESCRIPT)
    system_events = run_osascript(SYSTEM_EVENTS_SCRIPT)
    result = {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "after": after.isoformat(timespec="seconds"),
        "safari_raw": safari,
        "safari": parse_lines(str(safari.get("stdout", ""))),
        "system_events_raw": system_events,
        "system_events": parse_lines(str(system_events.get("stdout", ""))),
        "recent_downloads": recent_downloads(after),
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out_json:
        out = ROOT / args.out_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {out}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
