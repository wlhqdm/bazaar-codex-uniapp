from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zh_translate import (
    translate_en_to_zh,
    translate_enchant_name,
    translate_event_name,
    translate_tags,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "src" / "data"
IMAGE_DIR = ROOT / "src" / "static" / "cards" / "vanessa"
SOURCE_URL = "https://bazaarwinner.com/hero/vanessa"
ITEM_URL_TEMPLATE = "https://bazaarwinner.com/item/{slug}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CursorAgent/1.0"


CARD_PATTERN = re.compile(
    r'<a class="card[^"]*" href="/item/(?P<slug>[^"]+)">'
    r'.*?<img src="(?P<image>[^"]+)" alt="(?P<nameZh>[^"]+)"'
    r'.*?<span class="absolute top-1 left-1 chip text-\[10px\] tier-(?P<tier>[A-Za-z]+) bg-black/60">(?P<tierZh>.*?)</span>'
    r'(?P<headerExtras>.*?)'
    r'<div class="font-medium text-sm leading-tight group-hover:text-amber-300 truncate">(?P<nameZhText>.*?)</div>'
    r'.*?<div class="text-\[11px\] text-\[var\(--text-dim\)\] truncate">(?P<nameEn>.*?)</div>'
    r'.*?<div class="flex items-center gap-1 flex-wrap mt-1.5">(?P<tags>.*?)</div>'
    r"</div></a>",
    re.S,
)
TAG_PATTERN = re.compile(r"<span class=\"chip text-\[10px\]\">(.*?)</span>")
DAY_BADGE_PATTERN = re.compile(r">D<!-- -->(?P<day>\d+)<!-- -->\+<")
DAY_SUPPLEMENT_PATTERN = re.compile(r'title="数据补充：来自社区牌组反推"[^>]*>补</span>')
DETAIL_DAY_PATTERN = re.compile(r"第 <!-- -->(?P<day>\d+)<!-- --> 天起可获得")
DETAIL_EFFECTS_PATTERN = re.compile(
    r'<section class="card p-5"><h2 class="text-base font-semibold mb-3">.*?</h2><div class="space-y-3">(?P<body>.*?)</div></section>',
    re.S,
)
DETAIL_TIER_BLOCK_PATTERN = re.compile(
    r'<div><div class="text-sm font-medium mb-1 tier-(?P<tier>[A-Za-z]+)">(?P<tierZh>.*?)</div><ul class="text-sm space-y-1 text-\[var\(--text\)\]">(?P<items>.*?)</ul></div>',
    re.S,
)
DETAIL_LIST_ITEM_PATTERN = re.compile(r"<li class=\"leading-relaxed\">(.*?)</li>")
DETAIL_SOURCE_PATTERN = re.compile(
    r'<section class="card p-5"><h2 class="text-base font-semibold mb-3">.*?<span class="text-xs text-\[var\(--text-dim\)\] font-normal">.*?</span></h2>(?P<body>.*?)</section>',
    re.S,
)
DETAIL_SOURCE_ITEM_PATTERN = re.compile(
    r'<li class="flex items-baseline gap-2"><span class="font-medium text-amber-200 shrink-0">(.*?)</span><span class="text-\[var\(--text-dim\)\] text-xs">(.*?)</span></li>',
    re.S,
)
DETAIL_EVENT_PATTERN = re.compile(
    r'<h3 class="text-sm font-semibold mt-4 mb-2">出现于战斗事件</h3>'
    r'<ul class="text-sm space-y-1 text-\[var\(--text-dim\)\]">(?P<body>.*?)</ul>',
    re.S,
)
DETAIL_EVENT_ITEM_PATTERN = re.compile(r"<li>(.*?)</li>")
DETAIL_ENCHANT_PATTERN = re.compile(
    r'<section class="card p-5 mt-6"><h2 class="text-base font-semibold mb-3">附魔变体</h2>'
    r'<div class="grid[^"]*">(?P<body>.*?)</div></section>',
    re.S,
)
DETAIL_ENCHANT_BLOCK_PATTERN = re.compile(
    r'<div class="bg-\[var\(--bg-soft\)\] rounded p-3 border border-\[var\(--border\)\]">'
    r'<div class="font-medium text-amber-200 mb-1">(?P<name>.*?)</div>'
    r'<ul class="text-xs space-y-0\.5 text-\[var\(--text\)\]">(?P<items>.*?)</ul></div>',
    re.S,
)
DETAIL_ENCHANT_LINE_PATTERN = re.compile(r"<li>(.*?)</li>")
DETAIL_TEXT_BLOCK_PATTERN = re.compile(r'<div class="text-sm text-\[var\(--text-dim\)\]">(.*?)</div>')
SIZE_EN = {"小": "Small", "中": "Medium", "大": "Large"}

TRANSLATE_CACHE_PATH = DATA_DIR / "translation-cache.json"


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        return response.read().decode("utf-8")


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        return response.read()


def clean(value: str) -> str:
    return unescape(re.sub(r"\s+", " ", value)).strip()


def load_translate_cache() -> dict[str, str]:
    if TRANSLATE_CACHE_PATH.exists():
        try:
            return json.loads(TRANSLATE_CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_translate_cache(cache: dict[str, str]) -> None:
    TRANSLATE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATE_CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def svg_placeholder(title: str, subtitle: str) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_subtitle = subtitle.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <rect width="600" height="400" fill="#1f2430" />
  <rect x="20" y="20" width="560" height="360" rx="20" fill="#2b3245" stroke="#d6a85f" stroke-width="4" />
  <text x="300" y="185" text-anchor="middle" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" font-size="42" fill="#f5e4c3">{safe_title}</text>
  <text x="300" y="235" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#d4d8e5">{safe_subtitle}</text>
  <text x="300" y="300" text-anchor="middle" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" font-size="20" fill="#aab1c6">封面源站缺失，已保留卡牌条目供后续替换</text>
</svg>"""


def parse_day_fields(header_html: str, fallback_day: int | None = None) -> dict:
    day_match = DAY_BADGE_PATTERN.search(header_html or "")
    if day_match:
        day = int(day_match.group("day"))
        return {
            "day": day,
            "dayLabel": f"D{day}+",
            "dayZh": f"第{day}天起可获得",
            "dayStatus": "official",
        }
    if DAY_SUPPLEMENT_PATTERN.search(header_html or ""):
        return {
            "day": None,
            "dayLabel": "补",
            "dayZh": "数据补充",
            "dayStatus": "community",
        }
    if fallback_day is not None:
        return {
            "day": fallback_day,
            "dayLabel": f"D{fallback_day}+",
            "dayZh": f"第{fallback_day}天起可获得",
            "dayStatus": "official",
        }
    return {
        "day": None,
        "dayLabel": "",
        "dayZh": "",
        "dayStatus": "unknown",
    }


def parse_cards(html: str) -> list[dict]:
    cards: list[dict] = []
    for index, match in enumerate(CARD_PATTERN.finditer(html), start=1):
        tags = [clean(tag) for tag in TAG_PATTERN.findall(match.group("tags"))]
        size_zh = tags[0] if tags else ""
        type_tags = tags[1:] if len(tags) > 1 else []
        day_fields = parse_day_fields(match.group("headerExtras"))
        cards.append(
            {
                "id": match.group("slug"),
                "slug": match.group("slug"),
                "hero": "Vanessa",
                "heroZh": "瓦内莎",
                "index": index,
                "nameZh": clean(match.group("nameZhText") or match.group("nameZh")),
                "nameEn": clean(match.group("nameEn")),
                "image": f"/static/cards/vanessa/{match.group('slug')}.avif",
                "remoteImage": match.group("image"),
                "tier": match.group("tier"),
                "tierZh": clean(match.group("tierZh")),
                "size": SIZE_EN.get(size_zh, ""),
                "sizeZh": size_zh,
                "tags": type_tags,
                "tagsZh": translate_tags(type_tags),
                **day_fields,
                "sourceStatus": "site_official_zh",
                "notes": "中文名为公开图鉴站标注的官方简体；效果说明为本站初版中文，后续可手动校对。",
            }
        )
    return cards


def parse_detail(card: dict) -> dict:
    html = fetch_text(ITEM_URL_TEMPLATE.format(slug=card["slug"]))
    detail = {
        "pageUrl": ITEM_URL_TEMPLATE.format(slug=card["slug"]),
        "effects": [],
        "sources": [],
        "events": [],
        "enchantments": [],
        "detailNotice": "",
        "day": None,
    }

    day_match = DETAIL_DAY_PATTERN.search(html)
    if day_match:
        detail["day"] = int(day_match.group("day"))

    effects_match = DETAIL_EFFECTS_PATTERN.search(html)
    if effects_match:
        effects_body = effects_match.group("body")
        tier_blocks = DETAIL_TIER_BLOCK_PATTERN.findall(effects_body)
        if tier_blocks:
            for tier, tier_zh, items_html in tier_blocks:
                # Effects are rendered in English on the source site; translate to Chinese (initial version).
                # Keep the original English lines as a fallback/reference.
                lines_en = [clean(item) for item in DETAIL_LIST_ITEM_PATTERN.findall(items_html)]
                detail["effects"].append(
                    {
                        "tier": clean(tier),
                        "tierZh": clean(tier_zh),
                        "linesEn": lines_en,
                        "linesZh": [],  # filled during enrichment
                    }
                )
        else:
            text_match = DETAIL_TEXT_BLOCK_PATTERN.search(effects_body)
            if text_match:
                detail["detailNotice"] = clean(text_match.group(1))

    source_match = DETAIL_SOURCE_PATTERN.search(html)
    if source_match:
        source_body = source_match.group("body")
        source_items = DETAIL_SOURCE_ITEM_PATTERN.findall(source_body)
        if source_items:
            detail["sources"] = [
                {
                    "type": "shop",
                    "name": clean(name),
                    "descriptionEn": clean(description),
                    "descriptionZh": "",  # filled during enrichment
                }
                for name, description in source_items
            ]
        else:
            text_match = DETAIL_TEXT_BLOCK_PATTERN.search(source_body)
            if text_match and not detail["detailNotice"]:
                detail["detailNotice"] = clean(text_match.group(1))

        event_match = DETAIL_EVENT_PATTERN.search(source_body)
        if event_match:
            detail["events"] = [
                {
                    "type": "event",
                    "name": clean(name),
                    "nameZh": clean(name),
                    "descriptionEn": "Appears in combat event",
                    "descriptionZh": "出现于战斗事件",
                }
                for name in DETAIL_EVENT_ITEM_PATTERN.findall(event_match.group("body"))
            ]

    enchant_match = DETAIL_ENCHANT_PATTERN.search(html)
    if enchant_match:
        for name, items_html in DETAIL_ENCHANT_BLOCK_PATTERN.findall(enchant_match.group("body")):
            lines_en = [clean(item) for item in DETAIL_ENCHANT_LINE_PATTERN.findall(items_html)]
            detail["enchantments"].append(
                {
                    "name": clean(name),
                    "nameZh": "",
                    "linesEn": lines_en,
                    "linesZh": [],
                }
            )

    return detail


def enrich_cards(cards: list[dict]) -> None:
    cache = load_translate_cache()
    for card in cards:
        detail = parse_detail(card)
        card["detailUrl"] = detail["pageUrl"]
        card["effects"] = detail["effects"]
        card["sources"] = detail["sources"]
        card["events"] = detail["events"]
        card["enchantments"] = detail["enchantments"]
        card["detailNotice"] = detail["detailNotice"]

        if detail.get("day") is not None and card.get("dayStatus") != "community":
            day = detail["day"]
            card["day"] = day
            card["dayLabel"] = f"D{day}+"
            card["dayZh"] = f"第{day}天起可获得"
            card["dayStatus"] = "official"

        for effect in card.get("effects", []):
            lines_en = effect.get("linesEn", []) or []
            lines_zh = []
            for line in lines_en:
                zh = cache.get(line) or translate_en_to_zh(line)
                cache[line] = zh
                lines_zh.append(zh)
            effect["linesZh"] = lines_zh
            effect["lines"] = lines_zh

        for source in card.get("sources", []):
            desc_en = source.get("descriptionEn", "") or ""
            zh = cache.get(desc_en) or translate_en_to_zh(desc_en)
            cache[desc_en] = zh
            source["descriptionZh"] = zh
            source["description"] = zh

        for event in card.get("events", []):
            event["nameZh"] = translate_event_name(event.get("name") or "")
            event["descriptionZh"] = "出现于战斗事件"
            event["description"] = event["descriptionZh"]

        for enchant in card.get("enchantments", []):
            enchant["nameZh"] = translate_enchant_name(enchant.get("name") or "")
            lines_en = enchant.get("linesEn", []) or []
            lines_zh = []
            for line in lines_en:
                zh = cache.get(line) or translate_en_to_zh(line)
                cache[line] = zh
                lines_zh.append(zh)
            enchant["linesZh"] = lines_zh
            enchant["lines"] = lines_zh

        if card.get("detailNotice"):
            zh = cache.get(card["detailNotice"]) or translate_en_to_zh(card["detailNotice"])
            cache[card["detailNotice"]] = zh
            card["detailNoticeZh"] = zh
        save_translate_cache(cache)


def download_images(cards: list[dict]) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for card in cards:
        extension = ".webp" if ".webp" in card["remoteImage"] else ".avif"
        output_path = IMAGE_DIR / f"{card['slug']}{extension}"
        if output_path.exists():
            card["image"] = f"/static/cards/vanessa/{output_path.name}"
            card["imageStatus"] = "downloaded"
            continue
        try:
            output_path.write_bytes(fetch_bytes(card["remoteImage"]))
            card["image"] = f"/static/cards/vanessa/{output_path.name}"
            card["imageStatus"] = "downloaded"
        except HTTPError:
            placeholder_path = IMAGE_DIR / f"{card['slug']}.svg"
            placeholder_path.write_text(
                svg_placeholder(card["nameZh"], card["nameEn"]),
                encoding="utf-8",
            )
            card["image"] = f"/static/cards/vanessa/{placeholder_path.name}"
            card["imageStatus"] = "placeholder"


def write_outputs(cards: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "hero": {
            "key": "vanessa",
            "nameZh": "瓦内莎",
            "nameEn": "Vanessa",
            "titleZh": "海盗",
            "count": len(cards),
            "sourceUrl": SOURCE_URL,
            "translationBasis": "BazaarWinner 页面标注为官方简体中文",
        },
        "cards": cards,
    }
    (DATA_DIR / "vanessa-cards.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    review_payload = {
        "summary": {
            "total": len(cards),
            "needsReview": 0,
            "missingImages": len([card for card in cards if card.get("imageStatus") == "placeholder"]),
            "basis": "BazaarWinner 页面标注为官方简体中文；当前版本未做游戏客户端逐卡复核",
        },
        "items": [
            {
                "id": card["id"],
                "nameZh": card["nameZh"],
                "nameEn": card["nameEn"],
                "issue": "image_missing_from_source",
                "resolution": "generated_placeholder",
            }
            for card in cards
            if card.get("imageStatus") == "placeholder"
        ],
    }
    (DATA_DIR / "vanessa-review.json").write_text(
        json.dumps(review_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    html = fetch_text(SOURCE_URL)
    cards = parse_cards(html)
    if len(cards) != 139:
        raise RuntimeError(f"Expected 139 cards, got {len(cards)}")
    enrich_cards(cards)
    download_images(cards)
    write_outputs(cards)
    print(f"Fetched {len(cards)} Vanessa cards.")


if __name__ == "__main__":
    main()
