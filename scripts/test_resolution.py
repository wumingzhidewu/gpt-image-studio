import json, base64, time, csv
from pathlib import Path
import openai, requests as rq
from PIL import Image

cfg = json.loads((Path.home() / ".gpt_image_studio" / "config.json").read_text("utf-8"))
client = openai.OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
out_dir = Path.home() / ".gpt_image_studio" / "images"
out_dir.mkdir(exist_ok=True)

PROMPT = "a majestic golden eagle flying over mountain peaks, ultra detailed, dramatic lighting"


def run(model, size, fmt, quality, n):
    params = dict(model=model, prompt=PROMPT, size=size,
                  output_format=fmt, quality=quality, n=n)
    label = f"{model}|{size}|q={quality}|n={n}"
    print(f"[TEST] {label}", flush=True)
    try:
        t0 = time.time()
        resp = client.images.generate(**params)
        elapsed = round(time.time() - t0, 1)
        saved = []
        for i, d in enumerate(resp.data):
            ts = int(time.time() * 1000)
            p = out_dir / f"res_{ts}_{i}.{fmt}"
            if d.b64_json:
                raw = base64.b64decode(d.b64_json)
                p.write_bytes(raw)
                saved.append(str(p))
            elif d.url:
                r = rq.get(d.url, timeout=120)
                r.raise_for_status()
                p.write_bytes(r.content)
                saved.append(str(p))

        # 读实际尺寸
        actual_sizes = []
        for p in saved:
            try:
                img = Image.open(p)
                actual_sizes.append(f"{img.width}x{img.height}")
            except Exception:
                actual_sizes.append("?")

        got_n = len(saved)
        n_match = got_n == n
        print(f"  -> OK  elapsed={elapsed}s  got={got_n}/{n}张  sizes={actual_sizes}", flush=True)
        return "OK", elapsed, got_n, "; ".join(actual_sizes), n_match, "; ".join(saved)
    except Exception as e:
        msg = str(e)[:220]
        print(f"  -> ERROR: {msg}", flush=True)
        return "ERROR", 0, 0, "", False, msg


# 测试矩阵
# gpt-image-2: 支持 1K/2K/4K，方形和非方形
# gpt-image-1/1.5: 最大 1536，只支持有限尺寸
CASES = [
    # ── gpt-image-2 分辨率测试 ──
    ("gpt-image-2", "1024x1024", "png", "low",    1),   # 1K 方形
    ("gpt-image-2", "2048x2048", "png", "medium", 1),   # 2K 方形
    ("gpt-image-2", "3840x2160", "png", "medium", 1),   # 4K 16:9
    ("gpt-image-2", "2160x3840", "png", "medium", 1),   # 4K 9:16
    ("gpt-image-2", "3840x3840", "png", "low",    1),   # 4K 方形
    ("gpt-image-2", "2048x1152", "png", "medium", 1),   # 2K 16:9
    ("gpt-image-2", "1152x2048", "png", "medium", 1),   # 2K 9:16
    ("gpt-image-2", "1024x576",  "png", "low",    1),   # 1K 16:9
    ("gpt-image-2", "576x1024",  "png", "low",    1),   # 1K 9:16
    # ── gpt-image-2 数量测试 ──
    ("gpt-image-2", "1024x1024", "png", "low",    2),
    ("gpt-image-2", "1024x1024", "png", "low",    3),
    ("gpt-image-2", "1024x1024", "png", "low",    4),
    # ── gpt-image-1 分辨率 ──
    ("gpt-image-1", "1024x1024", "png", "medium", 1),   # 1K 方形
    ("gpt-image-1", "1024x1536", "png", "medium", 1),   # 1.5K 竖
    ("gpt-image-1", "1536x1024", "png", "medium", 1),   # 1.5K 横
    ("gpt-image-1", "1536x1536", "png", "medium", 1),   # 1.5K 方形
    ("gpt-image-1", "2048x2048", "png", "medium", 1),   # 2K — 应该报错
    # ── gpt-image-1 数量测试 ──
    ("gpt-image-1", "1024x1024", "png", "low",    2),
    ("gpt-image-1", "1024x1024", "png", "low",    4),
    ("gpt-image-1", "1024x1024", "png", "low",    8),
    # ── gpt-image-1.5 ──
    ("gpt-image-1.5", "1024x1024", "png", "medium", 1),
    ("gpt-image-1.5", "1024x1536", "png", "medium", 1),
    ("gpt-image-1.5", "1536x1536", "png", "medium", 1),
    ("gpt-image-1.5", "1024x1024", "png", "low",    2),
    ("gpt-image-1.5", "1024x1024", "png", "low",    4),
]

rows = []
for model, size, fmt, quality, n in CASES:
    status, elapsed, got_n, actual_sz, n_match, paths = run(model, size, fmt, quality, n)
    rows.append([model, size, fmt, quality, n, status, elapsed,
                 got_n, n_match, actual_sz, paths])
    time.sleep(2)

csv_path = Path("F:/workspace/git/python/get-gpt-image/alpha_test_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["model", "requested_size", "format", "quality", "n_requested",
                "api_status", "elapsed_s", "n_received", "n_count_match",
                "actual_image_sizes", "image_paths"])
    w.writerows(rows)

print(f"\n[DONE] {len(rows)} rows -> {csv_path}")
print()
print(f"{'model':<14} {'size':<12} {'q':<8} {'n_req':>5} {'status':<8} {'t(s)':>6} "
      f"{'got':>4} {'match':>6} {'actual_size'}")
print("-" * 95)
for r in rows:
    match_str = "YES" if r[8] else ("N/A" if r[5] == "ERROR" else "NO !")
    actual = r[9][:30] if r[9] else "-"
    print(f"{r[0]:<14} {r[1]:<12} {r[3]:<8} {r[4]:>5} {r[5]:<8} {r[6]:>6} "
          f"{r[7]:>4} {match_str:>6}   {actual}")
