from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_translate import translate_en_to_zh, translate_tags

DATA_PATH = ROOT / "src" / "data" / "vanessa-cards.json"
REVIEW_PATH = ROOT / "src" / "data" / "vanessa-review.json"
CACHE_PATH = ROOT / "src" / "data" / "translation-cache.json"


def still_english(text: str) -> bool:
    cleaned = re.sub(r"\{aura\.\d+\}", "", text or "")
    return bool(re.search(r"[A-Za-z]{3,}", cleaned))


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    cache: dict[str, str] = {}
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

        notice = card.get("detailNotice") or ""
        if notice:
            zh = cache.get(notice) or translate_en_to_zh(notice)
            cache[notice] = zh
            card["detailNoticeZh"] = zh

    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

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
    REVIEW_PATH.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Translated {len(payload['cards'])} cards. Remaining English-like lines: {len(remaining)}")


if __name__ == "__main__":
    main()
