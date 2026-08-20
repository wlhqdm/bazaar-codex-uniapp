"""Incrementally enrich existing hero card JSON with day / events / enchantments."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_heroes import (  # noqa: E402
    get_hero,
    load_heroes,
    fetch_text,
    parse_cards,
    parse_detail,
    load_translate_cache,
    save_translate_cache,
)
from zh_translate import (  # noqa: E402
    translate_en_to_zh,
    translate_enchant_name,
    translate_event_name,
    translate_shop_name,
    translate_tags,
)

DATA_DIR = ROOT / "src" / "data"
SIZE_EN = {"小": "Small", "中": "Medium", "大": "Large"}


def apply_list_fields(card: dict, list_card: dict | None) -> None:
    if list_card:
        for key in ("day", "dayLabel", "dayZh", "dayStatus", "size", "sizeZh", "tags", "tagsZh"):
            if key in list_card:
                card[key] = list_card[key]
        return
    card.setdefault("size", SIZE_EN.get(card.get("sizeZh") or "", ""))
    card["tagsZh"] = translate_tags(card.get("tags") or [])


def apply_detail_fields(card: dict, detail: dict, cache: dict[str, str]) -> None:
    if detail.get("day") is not None and card.get("dayStatus") != "community":
        day = detail["day"]
        card["day"] = day
        card["dayLabel"] = f"D{day}+"
        card["dayZh"] = f"第{day}天起可获得"
        card["dayStatus"] = "official"

    for source in card.get("sources") or []:
        source.setdefault("type", "shop")
        source["nameZh"] = translate_shop_name(source.get("name") or "")

    events = detail.get("events") or []
    for event in events:
        event["nameZh"] = translate_event_name(event.get("name") or "")
        event["descriptionZh"] = "出现于战斗事件"
        event["description"] = event["descriptionZh"]
    card["events"] = events

    enchantments = detail.get("enchantments") or []
    for enchant in enchantments:
        enchant["nameZh"] = translate_enchant_name(enchant.get("name") or "")
        lines_en = enchant.get("linesEn") or []
        lines_zh = []
        for line in lines_en:
            zh = cache.get(line) or translate_en_to_zh(line)
            cache[line] = zh
            lines_zh.append(zh)
        enchant["linesZh"] = lines_zh
        enchant["lines"] = lines_zh
    card["enchantments"] = enchantments

    if detail.get("effects"):
        card["effects"] = detail["effects"]
        for effect in card["effects"]:
            lines_zh = []
            for line in effect.get("linesEn") or []:
                zh = cache.get(line) or translate_en_to_zh(line)
                cache[line] = zh
                lines_zh.append(zh)
            effect["linesZh"] = lines_zh
            effect["lines"] = lines_zh

    if detail.get("sources") is not None:
        card["sources"] = detail["sources"]
        for source in card["sources"]:
            source.setdefault("type", "shop")
            source["nameZh"] = translate_shop_name(source.get("name") or "")
            desc_en = source.get("descriptionEn") or ""
            zh = cache.get(desc_en) or translate_en_to_zh(desc_en)
            cache[desc_en] = zh
            source["descriptionZh"] = zh
            source["description"] = zh


def enrich_hero(key: str, workers: int = 8) -> None:
    hero = get_hero(key)
    data_path = DATA_DIR / f"{key}-cards.json"
    print(f"=== Enrich {key} ===", flush=True)
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    existing = {card["slug"]: card for card in payload["cards"]}

    list_html = fetch_text(hero["sourceUrl"])
    list_cards = {card["slug"]: card for card in parse_cards(list_html, hero)}
    print(f"List cards: {len(list_cards)}", flush=True)

    for slug, card in existing.items():
        apply_list_fields(card, list_cards.get(slug))

    cache = load_translate_cache()
    slugs = list(existing.keys())
    details: dict[str, dict] = {}

    print(f"Fetching details with {workers} workers...", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(parse_detail, existing[slug]): slug for slug in slugs}
        done = 0
        for future in as_completed(futures):
            slug = futures[future]
            try:
                details[slug] = future.result()
            except Exception as exc:  # noqa: BLE001
                print(f"Failed {slug}: {exc}", flush=True)
                details[slug] = {"day": None, "events": [], "enchantments": [], "effects": [], "sources": []}
            done += 1
            if done % 20 == 0 or done == len(slugs):
                print(f"Fetched {done}/{len(slugs)}", flush=True)

    for slug, card in existing.items():
        apply_detail_fields(card, details.get(slug) or {}, cache)

    save_translate_cache(cache)
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with_events = sum(1 for card in payload["cards"] if card.get("events"))
    with_enchants = sum(1 for card in payload["cards"] if card.get("enchantments"))
    with_day = sum(1 for card in payload["cards"] if card.get("dayLabel"))
    print(
        f"Done {key}. day={with_day}, events={with_events}, enchantments={with_enchants} / {len(payload['cards'])}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hero", default="all")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    if args.hero == "all":
        keys = [h["key"] for h in load_heroes()]
    else:
        keys = [x.strip() for x in args.hero.split(",") if x.strip()]

    for key in keys:
        enrich_hero(key, workers=args.workers)


if __name__ == "__main__":
    main()
