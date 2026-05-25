MODELS = ["gpt-image-2", "gpt-image-1.5", "gpt-image-1"]

# 宽高比定义：label -> (w_ratio, h_ratio)
ASPECT_RATIOS = {
    "方形 1:1":    (1, 1),
    "竖版 2:3":    (2, 3),
    "竖版 3:4":    (3, 4),
    "故事版 9:16":  (9, 16),
    "横版 4:3":    (4, 3),
    "横版 3:2":    (3, 2),
    "宽屏 16:9":   (16, 9),
}

# 分辨率档位：长边像素（短边按比例计算，保证都是 64 的倍数）
RESOLUTIONS = {
    "1K": 1024,
    "2K": 2048,
    "4K": 3840,
}

# gpt-image-1/1.5 支持最大长边 1536
RESOLUTIONS_LIMITED = {"1K": 1024, "1.5K": 1536}

QUALITY_OPTIONS    = ["auto", "low", "medium", "high"]
FORMAT_OPTIONS     = ["webp", "png", "jpeg"]
BACKGROUND_OPTIONS = ["auto", "opaque", "transparent"]

TRANSPARENT_MODELS = {"gpt-image-1", "gpt-image-1.5"}

def compute_size(aspect_label: str, res_label: str, model: str) -> str:
    """根据宽高比 + 分辨率档位计算合法的 size 字符串。"""
    ratio = ASPECT_RATIOS.get(aspect_label) or (1, 1)
    res_map = RESOLUTIONS if model == "gpt-image-2" else RESOLUTIONS_LIMITED
    long_edge = res_map.get(res_label, 1024)

    w_r, h_r = ratio
    if w_r >= h_r:
        w = long_edge
        h = int(round(long_edge * h_r / w_r))
    else:
        h = long_edge
        w = int(round(long_edge * w_r / h_r))

    w = max(w, 256); h = max(h, 256)
    return f"{w}x{h}"
