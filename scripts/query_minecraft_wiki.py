#!/usr/bin/env python3
"""Minimal Minecraft Wiki lookup for official localized names."""

import argparse
import json
import sys
import urllib.parse
import urllib.request


ENDPOINTS = {
    "en": "https://minecraft.wiki/api.php",
    "zh": "https://zh.minecraft.wiki/api.php",
}


def request(endpoint: str, params: dict[str, str]) -> dict:
    params = {**params, "format": "json", "formatversion": "2"}
    url = endpoint + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "storage-tech-translation/0.1"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def lookup_term(term: str, language: str) -> dict[str, str]:
    en_data = request(
        ENDPOINTS["en"],
        {
            "action": "query",
            "titles": term,
            "prop": "langlinks",
            "lllang": language,
            "lllimit": "max",
            "redirects": "1",
        },
    )
    page = (en_data.get("query", {}).get("pages") or [{}])[0]
    title = page.get("title", term)
    localized = ""
    langlinks = page.get("langlinks") or []
    if langlinks:
        localized = langlinks[0].get("title", "")

    if language == "zh" and localized:
        zh_data = request(
            ENDPOINTS["zh"],
            {
                "action": "query",
                "titles": localized,
                "prop": "info",
                "inprop": "varianttitles",
                "variant": "zh-cn",
                "redirects": "1",
            },
        )
        zh_page = (zh_data.get("query", {}).get("pages") or [{}])[0]
        localized = (zh_page.get("varianttitles") or {}).get("zh-cn", localized)

    return {
        "term": term,
        "english_title": title,
        "language": language,
        "localized_name": localized,
        "source": f"https://minecraft.wiki/w/{urllib.parse.quote(title.replace(' ', '_'))}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Minecraft Wiki for official localized names")
    parser.add_argument("--term", required=True, help="English Minecraft Wiki page title")
    parser.add_argument("--language", default="zh", help="Target language code, default zh")
    parser.add_argument("--format", choices=["tsv", "json"], default="tsv")
    args = parser.parse_args()

    try:
        result = lookup_term(args.term, args.language)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print("term\tenglish_title\tlanguage\tlocalized_name\tsource")
        print("\t".join(result.values()))


if __name__ == "__main__":
    main()
