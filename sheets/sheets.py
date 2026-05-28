#!/usr/bin/env python3
"""Google Sheets CLI using a service account.

Usage:
  sheets.py info <sheet_id_or_url>
  sheets.py tabs <sheet_id_or_url>
  sheets.py read <sheet_id_or_url> <tab> [--range A1:Z100] [--format tsv|csv|json]
  sheets.py write <sheet_id_or_url> <tab> <range> <tsv_file>
  sheets.py append <sheet_id_or_url> <tab> <tsv_file>
  sheets.py cell <sheet_id_or_url> <tab> <a1>
  sheets.py set-cell <sheet_id_or_url> <tab> <a1> <value>

Sheet ID or URL both accepted. Sheets must be shared (Editor for writes,
Viewer for reads) with the service account email printed by `info`.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", module="urllib3")

import gspread
from google.oauth2.service_account import Credentials

KEY_PATH = os.environ.get("SHEETS_KEY_PATH", "")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]


def client():
    if not KEY_PATH:
        sys.exit("Error: set SHEETS_KEY_PATH to the path of your service account JSON key.")
    creds = Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    return gspread.authorize(creds), creds


def extract_id(s):
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", s)
    return m.group(1) if m else s


def open_sheet(gc, sheet_id_or_url):
    return gc.open_by_key(extract_id(sheet_id_or_url))


def cmd_info(args):
    gc, creds = client()
    sh = open_sheet(gc, args.sheet)
    print(f"Title:   {sh.title}")
    print(f"ID:      {sh.id}")
    print(f"SA:      {creds.service_account_email}")
    print(f"URL:     {sh.url}")
    print(f"Tabs:    {len(sh.worksheets())}")
    for ws in sh.worksheets():
        print(f"  - {ws.title!r}  ({ws.row_count}x{ws.col_count})  gid={ws.id}")


def cmd_tabs(args):
    gc, _ = client()
    sh = open_sheet(gc, args.sheet)
    for ws in sh.worksheets():
        print(ws.title)


def _rows_to_output(rows, fmt):
    if fmt == "json":
        return json.dumps(rows, ensure_ascii=False, indent=2)
    if fmt == "csv":
        buf = io.StringIO()
        csv.writer(buf).writerows(rows)
        return buf.getvalue().rstrip("\n")
    # tsv default — replace tabs in cells with spaces to keep columns aligned
    return "\n".join("\t".join(str(c).replace("\t", " ") for c in r) for r in rows)


def cmd_read(args):
    gc, _ = client()
    sh = open_sheet(gc, args.sheet)
    ws = sh.worksheet(args.tab)
    rows = ws.get(args.range) if args.range else ws.get_all_values()
    print(_rows_to_output(rows, args.format))


def cmd_cell(args):
    gc, _ = client()
    ws = open_sheet(gc, args.sheet).worksheet(args.tab)
    print(ws.acell(args.a1).value or "")


def cmd_set_cell(args):
    gc, _ = client()
    ws = open_sheet(gc, args.sheet).worksheet(args.tab)
    ws.update_acell(args.a1, args.value)
    print(f"wrote {args.a1} = {args.value!r}")


def _read_tsv(path):
    if path == "-":
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    return [line.split("\t") for line in text.splitlines()]


def cmd_write(args):
    gc, _ = client()
    ws = open_sheet(gc, args.sheet).worksheet(args.tab)
    rows = _read_tsv(args.tsv_file)
    ws.update(range_name=args.range, values=rows)
    print(f"wrote {len(rows)} rows x {len(rows[0]) if rows else 0} cols to {args.tab}!{args.range}")


def cmd_append(args):
    gc, _ = client()
    ws = open_sheet(gc, args.sheet).worksheet(args.tab)
    rows = _read_tsv(args.tsv_file)
    ws.append_rows(rows, value_input_option="USER_ENTERED")
    print(f"appended {len(rows)} rows to {args.tab}")


def main():
    p = argparse.ArgumentParser(description="Google Sheets CLI (service account)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info", help="Show sheet title, tabs, SA email")
    s.add_argument("sheet")
    s.set_defaults(func=cmd_info)

    s = sub.add_parser("tabs", help="List tab names (one per line)")
    s.add_argument("sheet")
    s.set_defaults(func=cmd_tabs)

    s = sub.add_parser("read", help="Read a tab or range")
    s.add_argument("sheet")
    s.add_argument("tab")
    s.add_argument("--range", help="A1 range (e.g. A1:D100). Default: whole tab")
    s.add_argument("--format", choices=["tsv", "csv", "json"], default="tsv")
    s.set_defaults(func=cmd_read)

    s = sub.add_parser("cell", help="Read a single cell")
    s.add_argument("sheet")
    s.add_argument("tab")
    s.add_argument("a1")
    s.set_defaults(func=cmd_cell)

    s = sub.add_parser("set-cell", help="Write a single cell")
    s.add_argument("sheet")
    s.add_argument("tab")
    s.add_argument("a1")
    s.add_argument("value")
    s.set_defaults(func=cmd_set_cell)

    s = sub.add_parser("write", help="Write a TSV block to a range (use - for stdin)")
    s.add_argument("sheet")
    s.add_argument("tab")
    s.add_argument("range")
    s.add_argument("tsv_file")
    s.set_defaults(func=cmd_write)

    s = sub.add_parser("append", help="Append TSV rows to bottom of tab (use - for stdin)")
    s.add_argument("sheet")
    s.add_argument("tab")
    s.add_argument("tsv_file")
    s.set_defaults(func=cmd_append)

    args = p.parse_args()
    try:
        args.func(args)
    except gspread.exceptions.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)
    except gspread.exceptions.WorksheetNotFound:
        print(f"Tab not found: {args.tab}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
