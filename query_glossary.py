#!/usr/bin/env python3
"""Query the local storage-tech glossary."""

import argparse
import csv
import json
from pathlib import Path


DEFAULT_GLOSSARY = Path(__file__).resolve().parent.parent / "references" / "glossary.csv"


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def score_row(row: dict[str, str], query: str) -> int:
    q = normalize(query)
    english = normalize(row.get("english", ""))
    short = normalize(row.get("short", ""))
    zh = normalize(row.get("zh", ""))
    if q == english or (short and q == short):
        return 100
    if q in english or (short and q in short):
        return 80
    if q in zh:
        return 70
    if all(part in english for part in q.split()):
        return 50
    return 0


def query(rows: list[dict[str, str]], term: str, limit: int) -> list[dict[str, str]]:
    scored = [(score_row(row, term), row) for row in rows]
    matches = [row for score, row in sorted(scored, key=lambda item: item[0], reverse=True) if score > 0]
    return matches[:limit]


def format_tsv(rows: list[dict[str, str]]) -> str:
    fields = ["english", "short", "zh", "keep_english", "domain", "notes"]
    out = ["\t".join(fields)]
    for row in rows:
        out.append("\t".join(row.get(field, "") for field in fields))
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the local storage-tech glossary")
    parser.add_argument("term", help="English, abbreviation, or Chinese term to query")
    parser.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    parser.add_argument("--format", choices=["tsv", "json"], default="tsv")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    rows = query(load_rows(args.glossary), args.term, args.limit)
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    else:
        print(format_tsv(rows))


if __name__ == "__main__":
    main()
