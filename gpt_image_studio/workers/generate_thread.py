import base64
import io
import os
import time

import openai
import requests
from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal

from ..i18n import I18N
from ..logging_config import log
from ..models import TRANSPARENT_MODELS
from ..paths import IMAGES_DIR, ensure_app_dirs


class GenerateThread(QThread):
    finished = pyqtSignal(list)
    error    = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, cfg, prompt, n, size, quality, fmt, background,
                 input_images, thinking, ctx_image_path, parent=None):
        super().__init__(parent)
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.cfg = cfg; self.prompt = prompt; self.n = n
        self.size = size; self.quality = quality; self.fmt = fmt
        self.background = background       # "auto" / "opaque" / "transparent"
        self.input_images = input_images   # 用户手动上传的参考图
        self.thinking = thinking
        self.ctx_image_path = ctx_image_path  # 上一轮自动传入的上下文图

    def run(self):
        try:
            client = openai.OpenAI(
                api_key=self.cfg["api_key"],
                base_url=self.cfg.get("base_url", "https://api.openai.com/v1"),
            )
            model   = self.cfg.get("model", "gpt-image-2")
            quality = "high" if (self.thinking and model == "gpt-image-2") else self.quality

            # 确定实际使用的参考图：用户上传优先，其次是上下文图
            ref_image = self.input_images[0] if self.input_images else self.ctx_image_path

            use_edit = ref_image is not None and os.path.exists(ref_image)

            # ── 打印请求日志 ──
            log.info("=" * 60)
            log.info(f"[REQUEST] endpoint : {'images.edit' if use_edit else 'images.generate'}")
            log.info(f"[REQUEST] model    : {model}")
            log.info(f"[REQUEST] prompt   : {self.prompt!r}")
            log.info(f"[REQUEST] size     : {self.size}")
            log.info(f"[REQUEST] quality  : {quality}")
            log.info(f"[REQUEST] format   : {self.fmt}")
            log.info(f"[REQUEST] n          : {self.n}")
            log.info(f"[REQUEST] thinking   : {self.thinking}")
            log.info(f"[REQUEST] background : {self.background}")
            if use_edit:
                log.info(f"[REQUEST] ref_img   : {ref_image}")
                log.info(f"[REQUEST] img_src   : {'user_upload' if self.input_images else 'context_auto'}")
            log.info("=" * 60)

            self.progress.emit(self._tr("connecting"))
            actual_fmt = self.fmt   # 可能因 transparent 而被修正为 png

            if use_edit:
                source = self._tr("user_upload") if self.input_images else self._tr("context_auto")
                self.progress.emit(self._tr("uploading_ref").format(source=source))
                pil = Image.open(ref_image).convert("RGBA")
                buf = io.BytesIO()
                pil.save(buf, format="PNG"); buf.seek(0)

                req_params = dict(
                    model=model,
                    image=("image.png", buf, "image/png"),
                    prompt=self.prompt,
                    n=self.n,
                    size=self.size,
                )
                log.info(f"[EDIT PARAMS] {dict((k,v) for k,v in req_params.items() if k != 'image')}")
                response = client.images.edit(**req_params)
            else:
                self.progress.emit(self._tr("generating_wait"))
                req_params = dict(
                    model=model,
                    prompt=self.prompt,
                    n=self.n,
                    size=self.size,
                    quality=quality,
                    output_format=self.fmt,
                )
                # background 仅 gpt-image-1/1.5 支持；transparent 强制 png/webp
                if model in TRANSPARENT_MODELS and self.background != "auto":
                    req_params["background"] = self.background
                    if self.background == "transparent" and self.fmt == "jpeg":
                        req_params["output_format"] = "png"
                        actual_fmt = "png"
                        log.warning("[WARN] transparent 不支持 jpeg，已自动切换为 png")
                log.info(f"[GENERATE PARAMS] {req_params}")
                response = client.images.generate(**req_params)

            log.info(f"[RESPONSE] received {len(response.data)} image(s)")

            results = []
            save_ext = actual_fmt if actual_fmt in ("png", "webp") else ("png" if use_edit else "jpeg")
            for i, img_data in enumerate(response.data):
                ext   = save_ext
                fname = IMAGES_DIR / f"{int(time.time()*1000)}_{i}.{ext}"
                if hasattr(img_data, "b64_json") and img_data.b64_json:
                    raw = base64.b64decode(img_data.b64_json)
                    fname.write_bytes(raw)
                    log.info(f"[SAVE] b64 -> {fname}  ({len(raw)//1024} KB)")
                elif hasattr(img_data, "url") and img_data.url:
                    log.info(f"[DOWNLOAD] {img_data.url[:80]}…")
                    r = requests.get(img_data.url, timeout=120); r.raise_for_status()
                    fname.write_bytes(r.content)
                    log.info(f"[SAVE] url -> {fname}  ({len(r.content)//1024} KB)")
                else:
                    log.warning(f"[SKIP] image[{i}] has no b64_json or url")
                    continue
                results.append(str(fname))

            log.info(f"[DONE] saved {len(results)} file(s)")
            self.progress.emit(self._tr("thread_done_count").format(count=len(results)))
            self.finished.emit(results)

        except Exception as e:
            log.error(f"[ERROR] {e}", exc_info=True)
            self.error.emit(str(e))

