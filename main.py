import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gpt_image_studio.app import main
from gpt_image_studio.models import (
    ASPECT_RATIOS,
    BACKGROUND_OPTIONS,
    FORMAT_OPTIONS,
    MODELS,
    QUALITY_OPTIONS,
    RESOLUTIONS,
    RESOLUTIONS_LIMITED,
    TRANSPARENT_MODELS,
    compute_size,
)

__all__ = [
    "main",
    "compute_size",
    "MODELS",
    "ASPECT_RATIOS",
    "RESOLUTIONS",
    "RESOLUTIONS_LIMITED",
    "QUALITY_OPTIONS",
    "FORMAT_OPTIONS",
    "BACKGROUND_OPTIONS",
    "TRANSPARENT_MODELS",
]


if __name__ == "__main__":
    main()
