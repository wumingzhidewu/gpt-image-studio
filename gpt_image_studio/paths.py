import sys
from pathlib import Path

APP_DIR = Path.home() / ".gpt_image_studio"
CONFIG_PATH = APP_DIR / "config.json"
SESSIONS_DIR = APP_DIR / "sessions"
IMAGES_DIR = APP_DIR / "images"
PROJECT_DIR = Path(__file__).resolve().parents[1]


def resource_path(*parts: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).joinpath(*parts)
    return PROJECT_DIR.joinpath(*parts)


ASSETS_DIR = resource_path("assets")
LOGO_PATH = ASSETS_DIR / "app_logo.png"
TEMPLATE_DIR = ASSETS_DIR / "templates"

def ensure_app_dirs() -> None:
    for d in (APP_DIR, SESSIONS_DIR, IMAGES_DIR):
        d.mkdir(parents=True, exist_ok=True)
