import csv, numpy as np
from pathlib import Path
from PIL import Image

out_dir = Path.home() / ".gpt_image_studio" / "images"

# results from test run
files = [
    ("gpt-image-1",  "1024x1024","auto",  "png", "medium",1,False,"rgba_explicit",   "exp_1779184814884_0.png"),
    ("gpt-image-1",  "1024x1024","auto",  "png", "high",  1,False,"product_cutout",  "exp_1779184850267_0.png"),
    ("gpt-image-1",  "1024x1024","auto",  "png", "medium",1,False,"sticker",         "exp_1779184916697_0.png"),
    ("gpt-image-1",  "1024x1024","auto",  "webp","medium",1,False,"logo_vector",      "exp_1779184976310_0.webp"),
    ("gpt-image-1",  "1024x1024","auto",  "png", "low",   1,False,"icon_flat",        "exp_1779185038344_0.png"),
    ("gpt-image-1",  "1024x1024","opaque","png", "medium",1,False,"rgba_explicit",   "exp_1779185086398_0.png"),
    ("gpt-image-1",  "1024x1024","opaque","png", "high",  1,False,"product_cutout",  "exp_1779185125868_0.png"),
    ("gpt-image-1",  "1024x1536","auto",  "png", "high",  1,False,"product_cutout",  "exp_1779185177791_0.png"),
    ("gpt-image-1",  "1536x1024","auto",  "png", "medium",1,False,"sticker",         "exp_1779185229720_0.png"),
    ("gpt-image-1",  "1024x1024","auto",  "png", "low",   2,False,"icon_flat",        "exp_1779185265249_0.png"),
    ("gpt-image-1.5","1024x1024","auto",  "png", "medium",1,False,"rgba_explicit",   "exp_1779185321645_0.png"),
    ("gpt-image-1.5","1024x1024","opaque","png", "high",  1,False,"product_cutout",  "exp_1779185384274_0.png"),
    ("gpt-image-1.5","1024x1024","auto",  "png", "medium",1,False,"sticker",         "exp_1779185449106_0.png"),
    ("gpt-image-1.5","1024x1024","auto",  "webp","medium",1,False,"logo_vector",      "exp_1779185471934_0.webp"),
    ("gpt-image-2",  "1024x1024","none",  "png", "low",   1,False,"rgba_explicit",   "exp_1779185489796_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "medium",1,False,"product_cutout",  "exp_1779185548697_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "low",   1,False,"sticker",         "exp_1779185587979_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "low",   1,False,"icon_flat",        "exp_1779185648412_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "high",  1,True, "rgba_explicit",   "exp_1779185697369_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "high",  1,True, "product_cutout",  "exp_1779185758071_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "high",  1,True, "sticker_thinking","exp_1779185815200_0.png"),
    ("gpt-image-2",  "1024x1024","none",  "png", "high",  1,True, "icon_flat",        "exp_1779185851311_0.png"),
    ("gpt-image-2",  "1024x1536","none",  "png", "medium",1,False,"product_cutout",  "exp_1779185895875_0.png"),
    ("gpt-image-2",  "2048x2048","none",  "png", "low",   1,False,"sticker",         "exp_1779185966823_0.png"),
]

# transparent API blocked — record separately
transparent_blocked = [
    ("gpt-image-1",  "1024x1024","transparent","png","medium",1,False,"rgba_explicit",  "API_502_BLOCKED"),
    ("gpt-image-1",  "1024x1024","transparent","png","high",  1,False,"product_cutout", "API_502_BLOCKED"),
    ("gpt-image-1.5","1024x1024","transparent","png","medium",1,False,"rgba_explicit",  "API_502_BLOCKED"),
    ("gpt-image-1.5","1024x1024","transparent","webp","high", 1,False,"sticker",        "API_502_BLOCKED"),
    ("gpt-image-2",  "1024x1024","transparent","png","low",   1,False,"rgba_explicit",  "API_502_BLOCKED"),
]

PROMPT_TEXTS = {
    "rgba_explicit":
        "PNG image with RGBA transparent background, alpha channel, fully transparent canvas, no background fill, isolated object only",
    "product_cutout":
        "professional product photo of a golden trophy cup, cutout style, remove background, isolated on transparent background, alpha channel PNG",
    "sticker":
        "cute cartoon cat sticker design, thick white outline, subject isolated on transparent background, no fill behind subject, sticker PNG",
    "logo_vector":
        "minimal flat logo, blue geometric hexagon shape, white inner lines, transparent background, vector style, alpha channel, no background",
    "icon_flat":
        "flat design app icon of a camera, white icon on fully transparent background, clean edges, alpha channel, no shadow, icon PNG",
    "sticker_thinking":
        "Create a sticker of a cute shiba inu dog with a happy expression, transparent background with only the dog and a thin white border, PNG with alpha channel transparency",
}


def analyze(fname):
    p = out_dir / fname
    if not p.exists():
        return "MISSING", "", 0.0, 0.0, 0.0, "N/A"
    img = Image.open(p)
    mode = img.mode
    arr = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    total = alpha.size
    t_pct  = round(float((alpha == 0).sum()) / total * 100, 1)
    s_pct  = round(float(((alpha > 0) & (alpha < 255)).sum()) / total * 100, 1)
    a_mean = round(float(alpha.mean()), 1)
    a_min  = int(alpha.min())
    has    = a_min < 255
    verdict = "TRUE_TRANSPARENT" if has and t_pct > 5 else ("SEMI" if has else "OPAQUE")
    return "OK", mode, t_pct, s_pct, a_mean, verdict


rows = []
for model, size, bg, fmt, q, n, think, pk, fname in files:
    api_status, mode, t_pct, s_pct, a_mean, verdict = analyze(fname)
    full = str(out_dir / fname)
    rows.append([model, size, bg, fmt, q, n, think, pk,
                 PROMPT_TEXTS.get(pk, ""), "OK", api_status,
                 mode, t_pct, s_pct, a_mean, verdict, full])

for model, size, bg, fmt, q, n, think, pk, note in transparent_blocked:
    rows.append([model, size, bg, fmt, q, n, think, pk,
                 PROMPT_TEXTS.get(pk, ""), "API_BLOCKED_502", "N/A",
                 "", "", "", "", "BLOCKED", note])

csv_path = Path("F:/workspace/git/python/get-gpt-image/alpha_test_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "size", "background_param", "output_format", "quality", "n", "thinking",
                "prompt_key", "prompt_text", "api_call_status", "img_read_status",
                "img_mode", "transparent_pct", "semi_transparent_pct", "alpha_mean",
                "alpha_verdict", "image_path"])
    w.writerows(rows)

print(f"Written {len(rows)} rows -> {csv_path}")
print()
print(f"{'model':<14} {'q':<7} {'think':<6} {'bg':<12} {'prompt':<16} {'mode':<5} {'t%':>6} {'verdict'}")
print("-" * 95)
for r in rows:
    verdict = r[15]
    marker = " *** TRUE TRANSPARENT ***" if verdict == "TRUE_TRANSPARENT" else ""
    print(f"{r[0]:<14} {r[4]:<7} {str(r[6]):<6} {r[2]:<12} {r[7]:<16} {str(r[11]):<5} "
          f"{str(r[12]):>6}% {verdict}{marker}")
