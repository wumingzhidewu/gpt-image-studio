import argparse
import base64
import sys
from pathlib import Path

import openai
import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gpt_image_studio.config import load_config
from gpt_image_studio.models import compute_size
from gpt_image_studio.templates import XIAOHONGSHU_TEMPLATES


def save_image(image_data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if getattr(image_data, "b64_json", None):
        path.write_bytes(base64.b64decode(image_data.b64_json))
        return
    if getattr(image_data, "url", None):
        response = requests.get(image_data.url, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
        return
    raise RuntimeError("Image response did not include b64_json or url")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Xiaohongshu template thumbnail images.")
    parser.add_argument("--force", action="store_true", help="Regenerate existing images.")
    parser.add_argument("--quality", default="high", choices=["auto", "low", "medium", "high"])
    args = parser.parse_args()

    cfg = load_config()
    api_key = cfg.get("api_key")
    if not api_key:
        print("Missing API key. Open the app settings first and save your API config.")
        return 1

    model = cfg.get("model", "gpt-image-2")
    size = compute_size("竖版 3:4", "2K" if model == "gpt-image-2" else "1.5K", model)
    client = openai.OpenAI(
        api_key=api_key,
        base_url=cfg.get("base_url", "https://api.openai.com/v1"),
    )

    generated = 0
    skipped = 0
    for index, template in enumerate(XIAOHONGSHU_TEMPLATES, 1):
        image_path = Path(template["image"])
        if image_path.exists() and not args.force:
            print(f"[{index}/{len(XIAOHONGSHU_TEMPLATES)}] skip existing: {image_path.name}")
            skipped += 1
            continue

        print(f"[{index}/{len(XIAOHONGSHU_TEMPLATES)}] generate: {template['title']} -> {image_path.name}")
        response = client.images.generate(
            model=model,
            prompt=template["prompt"],
            n=1,
            size=size,
            quality=args.quality,
            output_format="png",
        )
        save_image(response.data[0], image_path)
        generated += 1
        print(f"saved: {image_path}")

    print(f"Done. generated={generated}, skipped={skipped}, size={size}, model={model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
