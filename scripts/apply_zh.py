from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_translate import (
    translate_en_to_zh,
    translate_enchant_name,
    translate_event_name,
    translate_shop_name,
    translate_tags,
)

DATA_DIR = ROOT / "src" / "data"
HEROES_PATH = DATA_DIR / "heroes.json"
CACHE_PATH = DATA_DIR / "translation-cache.json"


def still_english(text: str) -> bool:
    cleaned = re.sub(r"\{aura\.\d+\}", "", text or "")
    return bool(re.search(r"[A-Za-z]{3,}", cleaned))


def load_hero_keys(selection: str) -> list[str]:
    heroes = json.loads(HEROES_PATH.read_text(encoding="utf-8"))["heroes"]
    if selection == "all":
        return [h["key"] for h in heroes]
    return [x.strip() for x in selection.split(",") if x.strip()]


def apply_one(data_path: Path, review_path: Path, cache: dict[str, str]) -> tuple[int, int]:
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    remaining: list[dict] = []

    for card in payload["cards"]:
        card["tagsZh"] = translate_tags(card.get("tags") or [])
        card["notes"] = "中文名为公开图鉴站标注的官方简体；效果说明为本站初版中文，后续可手动校对。"

        for effect in card.get("effects") or []:
            lines_en = effect.get("linesEn") or []
            lines_zh = []
            for line in lines_en:
                zh = cache.get(line) or translate_en_to_zh(line)
                cache[line] = zh
                lines_zh.append(zh)
                if still_english(zh):
                    remaining.append(
                        {
                            "id": card["id"],
                            "nameZh": card["nameZh"],
                            "nameEn": card["nameEn"],
                            "issue": "effect_needs_manual_zh",
                            "textEn": line,
                            "textZh": zh,
                        }
                    )
            effect["linesZh"] = lines_zh
            effect["lines"] = lines_zh

        for source in card.get("sources") or []:
            source.setdefault("type", "shop")
            source["nameZh"] = translate_shop_name(source.get("name") or "")
            desc_en = source.get("descriptionEn") or source.get("description") or ""
            zh = cache.get(desc_en) or translate_en_to_zh(desc_en)
            cache[desc_en] = zh
            source["descriptionZh"] = zh
            source["description"] = zh
            if still_english(zh):
                remaining.append(
                    {
                        "id": card["id"],
                        "nameZh": card["nameZh"],
                        "nameEn": card["nameEn"],
                        "issue": "source_needs_manual_zh",
                        "textEn": desc_en,
                        "textZh": zh,
                    }
                )

        for event in card.get("events") or []:
            event.setdefault("type", "event")
            event["nameZh"] = translate_event_name(event.get("name") or "")
            event["descriptionZh"] = "出现于战斗事件"
            event["description"] = event["descriptionZh"]

        for enchant in card.get("enchantments") or []:
            enchant["nameZh"] = translate_enchant_name(enchant.get("name") or "")
            lines_en = enchant.get("linesEn") or []
            lines_zh = []
            for line in lines_en:
                zh = cache.get(line) or translate_en_to_zh(line)
                cache[line] = zh
                lines_zh.append(zh)
                if still_english(zh):
                    remaining.append(
                        {
                            "id": card["id"],
                            "nameZh": card["nameZh"],
                            "nameEn": card["nameEn"],
                            "issue": "enchant_needs_manual_zh",
                            "textEn": line,
                            "textZh": zh,
                        }
                    )
            enchant["linesZh"] = lines_zh
            enchant["lines"] = lines_zh

        notice = card.get("detailNotice") or ""
        if notice:
            zh = cache.get(notice) or translate_en_to_zh(notice)
            cache[notice] = zh
            card["detailNoticeZh"] = zh

    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    image_issues = [
        {
            "id": card["id"],
            "nameZh": card["nameZh"],
            "nameEn": card["nameEn"],
            "issue": "image_missing_from_source",
            "resolution": "generated_placeholder",
        }
        for card in payload["cards"]
        if card.get("imageStatus") == "placeholder"
    ]
    review = {
        "summary": {
            "total": len(payload["cards"]),
            "needsReview": len(remaining),
            "missingImages": len(image_issues),
            "basis": "效果与来源为规则词典初版中文；仍含英文片段的条目已列入待复核。",
        },
        "items": image_issues + remaining[:200],
    }
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(payload["cards"]), len(remaining)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Chinese translations to hero card JSON")
    parser.add_argument("--hero", default="all", help="Hero key, comma-separated, or all")
    args = parser.parse_args()

    cache: dict[str, str] = {}
    if CACHE_PATH.exists():
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    total_cards = 0
    total_remaining = 0
    for key in load_hero_keys(args.hero):
        data_path = DATA_DIR / f"{key}-cards.json"
        if not data_path.exists():
            print(f"Skip {key}: missing {data_path.name}")
            continue
        review_path = DATA_DIR / f"{key}-review.json"
        cards, remaining = apply_one(data_path, review_path, cache)
        total_cards += cards
        total_remaining += remaining
        print(f"{key}: {cards} cards, remaining English-like: {remaining}")

    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done. Total cards={total_cards}, remaining={total_remaining}")


if __name__ == "__main__":
    main()
