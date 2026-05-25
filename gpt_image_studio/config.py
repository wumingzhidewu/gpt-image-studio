import json

from .paths import CONFIG_PATH, ensure_app_dirs


def load_config():
    ensure_app_dirs()
    if CONFIG_PATH.exists():
        cfg = json.loads(CONFIG_PATH.read_text("utf-8"))
    else:
        cfg = {"api_key": "", "base_url": "https://api.openai.com/v1"}
    cfg.setdefault("language", "zh")
    cfg.setdefault("theme", "dark")
    cfg.setdefault("default_aspect", "方形 1:1")
    cfg.setdefault("default_quality", "auto")
    if cfg.get("defaults_version") != 2:
        cfg["model"] = "gpt-image-2"
        cfg["default_resolution"] = "2K"
        cfg["default_format"] = "png"
        cfg["defaults_version"] = 2
        save_config(cfg)
    else:
        cfg.setdefault("model", "gpt-image-2")
        cfg.setdefault("default_resolution", "2K")
        cfg.setdefault("default_format", "png")
    return cfg


def save_config(cfg):
    ensure_app_dirs()
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), "utf-8")
