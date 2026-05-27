from __future__ import annotations

import re
import time
import uuid
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .paths import IMAGES_DIR, ensure_app_dirs

XHS_MODE = "xiaohongshu_graphic_text"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _short_title(topic: str) -> str:
    topic = re.sub(r"[\s，。！？、,.!?]+", "", topic.strip())
    if not topic:
        return "小红书图文选题"
    if len(topic) <= 18:
        return topic
    return topic[:18]


def _keywords(*values: str) -> list[str]:
    text = " ".join(v for v in values if v)
    raw = re.split(r"[\s，。！？、,.!?；;：:\n\r/|]+", text)
    seen = set()
    result = []
    for item in raw:
        item = item.strip("#《》【】（）()[]")
        if len(item) < 2 or item in seen:
            continue
        seen.add(item)
        result.append(item)
        if len(result) >= 6:
            break
    return result


def _hashtags(inputs: dict, keywords: list[str]) -> list[str]:
    base = ["小红书图文", "干货分享", "新手友好"]
    positioning = _clean(inputs.get("positioning"))
    audience = _clean(inputs.get("audience"))
    if positioning:
        base.insert(0, positioning[:12])
    if audience:
        base.append(audience[:12])
    base.extend(k[:12] for k in keywords[:3])
    tags = []
    for tag in base:
        tag = re.sub(r"\s+", "", tag.strip("#"))
        if tag and f"#{tag}" not in tags:
            tags.append(f"#{tag}")
        if len(tags) >= 8:
            break
    return tags[:8]


def build_local_xhs_draft(inputs: dict) -> dict:
    template_title = _clean(inputs.get("template_title"))
    template_prompt = _clean(inputs.get("template_prompt"))
    template_category = _clean(inputs.get("template_category"))
    topic = _clean(inputs.get("topic")) or template_title or "一个值得收藏的小红书选题"
    positioning = _clean(inputs.get("positioning")) or template_category or "真实经验分享"
    audience = _clean(inputs.get("audience")) or "正在找方法的人"
    goal = _clean(inputs.get("goal")) or "让读者收藏并评论"
    tone = _clean(inputs.get("tone")) or "真实、有用、像朋友聊天"
    key_points = _clean(inputs.get("key_points")) or template_prompt or "先讲痛点，再给方法，最后引导行动"
    avoid_words = _clean(inputs.get("avoid_words"))
    page_count = max(3, min(int(inputs.get("page_count") or 5), 8))
    visual_style = _clean(inputs.get("visual_style")) or template_category or "真实日常 / Authentic Daily Life"
    keywords = _keywords(topic, positioning, audience, key_points, template_prompt)
    title = _short_title(topic)
    opening = f"如果你也在关注「{title}」，这篇先帮你把思路理清。"
    body = [
        f"先别急着直接做图，先确认你的读者是谁：{audience}。内容越具体，越容易让人停下来。",
        f"这篇参考「{template_title or positioning}」模板展开，核心是 {key_points}。",
        f"最后把重点收束到一个可执行动作，让读者看完知道下一步怎么做，也更愿意收藏。",
    ]
    interaction = "你最想先优化哪一步？评论区告诉我，我继续拆。"
    risk_notes = ["避免绝对化承诺", "避免夸大收益或效果"]
    if avoid_words:
        risk_notes.append(f"避开这些表达：{avoid_words}")

    outline = [
        {
            "page_no": 1,
            "kind": "cover",
            "headline": title,
            "body": "",
            "description": f"封面突出主题《{title}》，给 {audience} 一个明确点击理由，风格：{visual_style}",
            "image_prompt": "",
            "status": "pending",
        }
    ]
    page_topics = [
        ("为什么值得看", f"点出痛点和场景：{audience} 为什么会需要这篇内容"),
        ("模板拆解", f"沿用「{template_title or title}」的视觉和内容方向，拆成读者能收藏的结构"),
        ("核心方法", f"拆解关键动作：{key_points}"),
        ("行动清单", f"给出可马上照做的步骤，目标：{goal}"),
        ("总结互动", interaction),
        ("收藏复盘", "用简短清单总结全文，适合截图收藏"),
        ("下一步", "引导读者评论自己的情况，方便后续选题延展"),
    ]
    for i in range(2, page_count + 1):
        headline, page_body = page_topics[i - 2]
        outline.append(
            {
                "page_no": i,
                "kind": "content",
                "headline": headline,
                "body": page_body,
                "description": page_body,
                "image_prompt": "",
                "status": "pending",
            }
        )

    draft = {
        "title": title,
        "opening_hook": opening,
        "body": body,
        "interaction_question": interaction,
        "hashtags": _hashtags(inputs, keywords),
        "risk_notes": risk_notes,
        "outline": outline,
    }
    for page in draft["outline"]:
        if page["kind"] == "cover":
            page["image_prompt"] = build_cover_prompt(draft, page, inputs, no_text=True)
        else:
            page["image_prompt"] = build_content_page_prompt(draft, page, inputs, no_text=True)
    return draft


def build_cover_prompt(draft: dict, page: dict, inputs: dict, *, no_text: bool) -> str:
    visual_style = _clean(inputs.get("visual_style")) or "真实日常 / Authentic Daily Life"
    topic = _clean(inputs.get("topic")) or draft.get("title", "小红书封面")
    text_rule = "no text, no Chinese characters, leave clean blank space for title overlay" if no_text else f"include accurate Chinese title text: {draft.get('title', '')}"
    return (
        f"小红书图文封面，3:4 竖版构图，主题：{topic}，风格：{visual_style}，"
        f"真实、有收藏感、移动端封面、高级但不商业硬广，{text_rule}，"
        "clear focal point, soft natural light, clean composition, editorial lifestyle cover"
    )


def build_content_page_prompt(draft: dict, page: dict, inputs: dict, *, no_text: bool) -> str:
    visual_style = _clean(inputs.get("visual_style")) or "真实日常 / Authentic Daily Life"
    text_rule = "no text, leave clean layout areas for local text overlay" if no_text else "minimal clean Chinese typography"
    return (
        f"小红书图文内容页，3:4 竖版，第{page.get('page_no')}页，"
        f"主题标题：{page.get('headline', '')}，画面内容：{page.get('description') or page.get('body', '')}，"
        f"整体风格与封面保持一致：{visual_style}，{text_rule}，"
        "simple visual hierarchy, warm realistic details, clean background, suitable for carousel note"
    )


def build_xhs_session(title: str, cfg: dict, inputs: dict, draft: dict) -> dict:
    now = _now()
    return {
        "id": str(uuid.uuid4()),
        "title": f"小红书：{title}",
        "created": now,
        "updated": now,
        "model": cfg.get("model", "gpt-image-2"),
        "mode": XHS_MODE,
        "xhs_version": 1,
        "xhs": {
            "inputs": inputs,
            "draft": {k: v for k, v in draft.items() if k != "outline"},
            "pages": draft.get("outline", []),
            "cover": {
                "title": title,
                "subtitle": "",
                "use_local_text_overlay": True,
            },
        },
        "turns": [],
    }


def update_page_image(session: dict, page_no: int, image_path: str, raw_image_path: str | None = None) -> None:
    now = _now()
    for page in session.get("xhs", {}).get("pages", []):
        if int(page.get("page_no", 0)) == int(page_no):
            page["final_image"] = image_path
            if raw_image_path:
                page["raw_image"] = raw_image_path
            page["status"] = "done"
            page["updated"] = now
            break
    session["updated"] = now


def append_xhs_turn(session: dict, page: dict, image_path: str, raw_image_path: str | None, prompt: str, cfg: dict, size: str, quality: str, background: str) -> None:
    turn = {
        "type": "xhs_cover" if page.get("kind") == "cover" else "xhs_content_page",
        "page_no": page.get("page_no"),
        "prompt": prompt,
        "model": cfg.get("model", "gpt-image-2"),
        "size": size,
        "quality": quality,
        "background": background,
        "images": [image_path],
        "timestamp": _now(),
    }
    if raw_image_path:
        turn["raw_images"] = [raw_image_path]
    session.setdefault("turns", []).append(turn)


def _font(size: int):
    for path in ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _wrap_text(text: str, max_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def render_text_overlay(image_path: str, title: str, subtitle: str = "") -> str:
    ensure_app_dirs()
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    box_h = int(h * 0.34)
    draw.rounded_rectangle(
        (int(w * 0.06), int(h * 0.07), int(w * 0.94), int(h * 0.07) + box_h),
        radius=max(24, int(w * 0.035)),
        fill=(255, 255, 255, 218),
    )
    title_font = _font(max(36, int(w * 0.075)))
    subtitle_font = _font(max(22, int(w * 0.04)))
    y = int(h * 0.11)
    for line in _wrap_text(title, 10)[:3]:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        x = int((w - (bbox[2] - bbox[0])) / 2)
        draw.text((x, y), line, font=title_font, fill=(22, 24, 32, 255))
        y += bbox[3] - bbox[1] + int(h * 0.012)
    if subtitle:
        y += int(h * 0.012)
        for line in _wrap_text(subtitle, 16)[:2]:
            bbox = draw.textbbox((0, 0), line, font=subtitle_font)
            x = int((w - (bbox[2] - bbox[0])) / 2)
            draw.text((x, y), line, font=subtitle_font, fill=(92, 99, 112, 255))
            y += bbox[3] - bbox[1] + 8
    final = Image.alpha_composite(img, overlay).convert("RGB")
    out = IMAGES_DIR / f"xhs_overlay_{int(time.time() * 1000)}.png"
    final.save(out, "PNG")
    return str(out)
