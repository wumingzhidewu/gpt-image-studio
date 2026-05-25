import json, base64, time, csv, io, sys
from pathlib import Path
import openai, requests as rq
from PIL import Image
import numpy as np

cfg = json.loads((Path.home() / ".gpt_image_studio" / "config.json").read_text("utf-8"))
client = openai.OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
out_dir = Path.home() / ".gpt_image_studio" / "images"
out_dir.mkdir(exist_ok=True)


def analyze_alpha(path):
    try:
        img = Image.open(path)
        mode = img.mode
        arr = np.array(img.convert("RGBA"))
        alpha = arr[:, :, 3]
        total = alpha.size
        t_pct  = round(float((alpha == 0).sum())   / total * 100, 1)
        s_pct  = round(float(((alpha > 0) & (alpha < 255)).sum()) / total * 100, 1)
        a_mean = round(float(alpha.mean()), 1)
        a_min  = int(alpha.min())
        has_real = a_min < 255
        if has_real and t_pct > 5:
            verdict = "TRUE_TRANSPARENT"
        elif has_real:
            verdict = "SEMI_TRANSPARENT"
        else:
            verdict = "OPAQUE"
        return mode, has_real, t_pct, s_pct, a_mean, verdict
    except Exception as e:
        return "ERROR", False, 0.0, 0.0, 0.0, "ERROR"


def run_case(model, prompt_key, prompt, size, background, fmt, quality, n, thinking):
    params = dict(model=model, prompt=prompt, size=size,
                  output_format=fmt, quality=quality, n=n)
    if background and background != "none":
        params["background"] = background
    label = f"{model}|{size}|bg={background}|fmt={fmt}|q={quality}|n={n}|think={thinking}"
    print(f"[TEST] {prompt_key} / {label}", flush=True)
    try:
        t0 = time.time()
        resp = client.images.generate(**params)
        elapsed = round(time.time() - t0, 1)
        saved = []
        for i, d in enumerate(resp.data):
            ts = int(time.time() * 1000)
            p = out_dir / f"exp_{ts}_{i}.{fmt}"
            if d.b64_json:
                raw = base64.b64decode(d.b64_json)
                p.write_bytes(raw)
                saved.append(str(p))
            elif d.url:
                r = rq.get(d.url, timeout=90)
                r.raise_for_status()
                p.write_bytes(r.content)
                saved.append(str(p))
        results = []
        for p in saved:
            mode, has_alpha, t_pct, s_pct, a_mean, verdict = analyze_alpha(p)
            print(f"  -> {Path(p).name}: mode={mode} alpha={has_alpha} "
                  f"transparent={t_pct}% semi={s_pct}% mean_a={a_mean} [{verdict}]", flush=True)
            results.append((p, mode, has_alpha, t_pct, s_pct, a_mean, verdict))
        return "OK", elapsed, results
    except Exception as e:
        msg = str(e)[:200]
        print(f"  -> ERROR: {msg}", flush=True)
        return "ERROR", 0, []


PROMPTS = {
    "rgba_explicit":
        "PNG image with RGBA transparent background, alpha channel, fully transparent canvas, "
        "no background fill, isolated object only",

    "product_cutout":
        "professional product photo of a golden trophy cup, white background cutout style, "
        "remove background, isolated on transparent background, alpha channel PNG",

    "sticker":
        "cute cartoon cat sticker design, thick white outline, "
        "subject isolated on transparent background, no fill behind subject, sticker PNG",

    "logo_vector":
        "minimal flat logo, blue geometric hexagon shape, white inner lines, "
        "transparent background, vector style, alpha channel, no background",

    "icon_flat":
        "flat design app icon of a camera, white icon on fully transparent background, "
        "clean edges, alpha channel, no shadow, icon PNG",

    "sticker_thinking":
        "Create a sticker of a cute shiba inu dog with a happy expression, "
        "the sticker should have a transparent background with only the dog and a thin white border visible. "
        "Output as PNG with alpha channel transparency.",
}

# (model, prompt_key, size, background, fmt, quality, n, thinking)
CASES = [
    # ── gpt-image-1, auto bg, varied prompts ──
    ("gpt-image-1", "rgba_explicit",   "1024x1024", "auto",   "png",  "medium", 1, False),
    ("gpt-image-1", "product_cutout",  "1024x1024", "auto",   "png",  "high",   1, False),
    ("gpt-image-1", "sticker",         "1024x1024", "auto",   "png",  "medium", 1, False),
    ("gpt-image-1", "logo_vector",     "1024x1024", "auto",   "webp", "medium", 1, False),
    ("gpt-image-1", "icon_flat",       "1024x1024", "auto",   "png",  "low",    1, False),
    # ── gpt-image-1, opaque bg explicit ──
    ("gpt-image-1", "rgba_explicit",   "1024x1024", "opaque", "png",  "medium", 1, False),
    ("gpt-image-1", "product_cutout",  "1024x1024", "opaque", "png",  "high",   1, False),
    # ── gpt-image-1, non-square ──
    ("gpt-image-1", "product_cutout",  "1024x1536", "auto",   "png",  "high",   1, False),
    ("gpt-image-1", "sticker",         "1536x1024", "auto",   "png",  "medium", 1, False),
    # ── gpt-image-1, n=2 ──
    ("gpt-image-1", "icon_flat",       "1024x1024", "auto",   "png",  "low",    2, False),
    # ── gpt-image-1.5, auto/opaque ──
    ("gpt-image-1.5", "rgba_explicit", "1024x1024", "auto",   "png",  "medium", 1, False),
    ("gpt-image-1.5", "product_cutout","1024x1024", "opaque", "png",  "high",   1, False),
    ("gpt-image-1.5", "sticker",       "1024x1024", "auto",   "png",  "medium", 1, False),
    ("gpt-image-1.5", "logo_vector",   "1024x1024", "auto",   "webp", "medium", 1, False),
    # ── gpt-image-2, no thinking ──
    ("gpt-image-2", "rgba_explicit",   "1024x1024", "none",   "png",  "low",    1, False),
    ("gpt-image-2", "product_cutout",  "1024x1024", "none",   "png",  "medium", 1, False),
    ("gpt-image-2", "sticker",         "1024x1024", "none",   "png",  "low",    1, False),
    ("gpt-image-2", "icon_flat",       "1024x1024", "none",   "png",  "low",    1, False),
    # ── gpt-image-2, thinking (quality=high) ──
    ("gpt-image-2", "rgba_explicit",   "1024x1024", "none",   "png",  "high",   1, True),
    ("gpt-image-2", "product_cutout",  "1024x1024", "none",   "png",  "high",   1, True),
    ("gpt-image-2", "sticker_thinking","1024x1024", "none",   "png",  "high",   1, True),
    ("gpt-image-2", "icon_flat",       "1024x1024", "none",   "png",  "high",   1, True),
    # ── gpt-image-2, non-square ──
    ("gpt-image-2", "product_cutout",  "1024x1536", "none",   "png",  "medium", 1, False),
    ("gpt-image-2", "sticker",         "2048x2048", "none",   "png",  "low",    1, False),
]

rows = []
for model, pk, size, bg, fmt, quality, n, thinking in CASES:
    status, elapsed, results = run_case(model, pk, PROMPTS[pk], size, bg, fmt, quality, n, thinking)
    if results:
        for img_path, mode, has_alpha, t_pct, s_pct, a_mean, verdict in results:
            rows.append([model, size, bg, fmt, quality, n, thinking, pk,
                         status, elapsed, mode, has_alpha, t_pct, s_pct, a_mean, verdict, img_path])
    else:
        rows.append([model, size, bg, fmt, quality, n, thinking, pk,
                     status, elapsed, "", "", "", "", "", "N/A", ""])
    time.sleep(2)

csv_path = Path("F:/workspace/git/python/get-gpt-image/test_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "size", "background", "output_format", "quality", "n", "thinking",
                "prompt_key", "status", "elapsed_s", "img_mode", "has_alpha",
                "transparent_pct", "semi_transparent_pct", "alpha_mean",
                "alpha_verdict", "image_path"])
    w.writerows(rows)

print(f"\n[DONE] {len(rows)} rows -> {csv_path}")

# 打印汇总
print("\n=== SUMMARY ===")
print(f"{'model':<14} {'q':<7} {'think':<6} {'bg':<7} {'prompt_key':<18} {'verdict':<18} {'t_pct':>7}")
for r in rows:
    if r[8] == "OK":
        print(f"{r[0]:<14} {r[4]:<7} {str(r[6]):<6} {r[2]:<7} {r[7]:<18} {r[15]:<18} {str(r[12]):>7}%")
    else:
        print(f"{r[0]:<14} {r[4]:<7} {str(r[6]):<6} {r[2]:<7} {r[7]:<18} ERROR")
