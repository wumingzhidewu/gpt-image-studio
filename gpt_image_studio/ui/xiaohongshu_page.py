from __future__ import annotations

import os
from datetime import datetime

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout, QWidget,
)

from ..config import load_config
from ..models import compute_size
from ..sessions import save_session
from ..templates import XIAOHONGSHU_TEMPLATES
from ..workers.generate_thread import GenerateThread
from ..xiaohongshu import XHS_MODE
from .image_widgets import ImageCard


class XiaohongshuTemplateCard(QFrame):
    selected = pyqtSignal(dict)
    activated = pyqtSignal(dict)

    def __init__(self, template: dict, parent=None):
        super().__init__(parent)
        self.template = template
        self.setObjectName("xhs-template-card")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumSize(210, 285)
        self.setMaximumWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        v = QVBoxLayout(self); v.setContentsMargins(8, 8, 8, 8); v.setSpacing(6)
        image = QLabel(); image.setObjectName("xhs-template-preview")
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setMinimumHeight(150)
        image.setMaximumHeight(190)
        image.setScaledContents(False)
        path = template.get("image")
        if path and Path(path).exists():
            pix = QPixmap(str(path)).scaled(
                280, 180,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            image.setPixmap(pix)
        v.addWidget(image)

        title = QLabel(template.get("title", "模板")); title.setObjectName("template-title")
        title.setWordWrap(True)
        v.addWidget(title)
        prompt = QLabel(template.get("prompt", "")); prompt.setObjectName("template-prompt")
        prompt.setWordWrap(True)
        prompt.setMaximumHeight(58)
        v.addWidget(prompt)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.selected.emit(self.template)

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.activated.emit(self.template)


class XiaohongshuPage(QWidget):
    def __init__(self, parent=None, on_sessions_changed=None, on_preview=None):
        super().__init__(parent)
        self.parent_window = parent
        self._tr = getattr(parent, "tr", lambda key: key)
        self.cfg = load_config()
        self.session = None
        self._worker = None
        self._on_sessions_changed = on_sessions_changed
        self._on_preview = on_preview
        self.selected_template = XIAOHONGSHU_TEMPLATES[0]
        self.selected_category = self.selected_template.get("category", "")
        self.template_cards = []
        self.setObjectName("xhs-page")
        self._build_ui()
        self.apply_template(self.selected_template)

    def _build_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(26, 22, 26, 16); root.setSpacing(14)
        header = QHBoxLayout()
        title_box = QVBoxLayout(); title_box.setSpacing(4); title_box.setContentsMargins(0, 0, 0, 0)
        self.title_lbl = QLabel(self._tr("xhs_title")); self.title_lbl.setObjectName("page-title")
        self.hint_lbl = QLabel(self._tr("xhs_simple_hint")); self.hint_lbl.setObjectName("section-hint")
        title_box.addWidget(self.title_lbl); title_box.addWidget(self.hint_lbl)
        header.addLayout(title_box); header.addStretch()
        self.new_btn = QPushButton(self._tr("xhs_new_note")); self.new_btn.setObjectName("header-action-btn")
        self.new_btn.clicked.connect(self.reset)
        header.addWidget(self.new_btn)
        root.addLayout(header)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")
        body = QWidget(); body.setStyleSheet("background:transparent;")
        self.body_layout = QVBoxLayout(body); self.body_layout.setContentsMargins(0, 0, 0, 0); self.body_layout.setSpacing(14)
        self.body_layout.addWidget(self._mk_template_card())
        self.body_layout.addWidget(self._mk_prompt_card())
        self.body_layout.addWidget(self._mk_results_card())
        self.body_layout.addStretch()
        scroll.setWidget(body)
        root.addWidget(scroll, 1)

    def _mk_template_card(self):
        card = QFrame(); card.setObjectName("xhs-step-card")
        v = QVBoxLayout(card); v.setContentsMargins(16, 14, 16, 14); v.setSpacing(12)
        h = QHBoxLayout()
        title = QLabel(self._tr("xhs_template_title")); title.setObjectName("section-heading")
        hint = QLabel(self._tr("xhs_simple_template_hint")); hint.setObjectName("section-hint")
        h.addWidget(title); h.addWidget(hint); h.addStretch()
        v.addLayout(h)

        self.templates_layout = QVBoxLayout(); self.templates_layout.setContentsMargins(0, 0, 0, 0); self.templates_layout.setSpacing(16)
        v.addLayout(self.templates_layout)
        self._render_templates()
        return card

    def _mk_prompt_card(self):
        card = QFrame(); card.setObjectName("xhs-step-card")
        v = QVBoxLayout(card); v.setContentsMargins(16, 14, 16, 14); v.setSpacing(10)
        h = QHBoxLayout()
        self.selected_label = QLabel("")
        self.selected_label.setObjectName("section-heading")
        h.addWidget(self.selected_label)
        h.addStretch()
        one_label = QLabel(self._tr("xhs_one_image_only")); one_label.setObjectName("xhs-field-label")
        h.addWidget(one_label)
        v.addLayout(h)

        self.prompt_edit = QTextEdit()
        self.prompt_edit.setObjectName("prompt-input")
        self.prompt_edit.setMinimumHeight(160)
        self.prompt_edit.setPlaceholderText(self._tr("xhs_prompt_placeholder"))
        v.addWidget(self.prompt_edit)

        actions = QHBoxLayout(); actions.addStretch()
        self.generate_btn = QPushButton(self._tr("xhs_generate_images")); self.generate_btn.setObjectName("xhs-generate-btn")
        self.generate_btn.setMinimumHeight(44)
        self._style_generate_button(False)
        self.generate_btn.clicked.connect(self.generate_images)
        actions.addWidget(self.generate_btn)
        v.addLayout(actions)
        return card

    def _mk_results_card(self):
        card = QFrame(); card.setObjectName("xhs-step-card")
        v = QVBoxLayout(card); v.setContentsMargins(16, 14, 16, 14); v.setSpacing(10)
        h = QHBoxLayout()
        title = QLabel(self._tr("current")); title.setObjectName("section-heading")
        hint = QLabel(self._tr("xhs_result_hint")); hint.setObjectName("section-hint")
        h.addWidget(title); h.addWidget(hint); h.addStretch(); v.addLayout(h)
        self.results_layout = QGridLayout(); self.results_layout.setContentsMargins(0, 0, 0, 0); self.results_layout.setSpacing(12)
        v.addLayout(self.results_layout)
        self.empty_results = QLabel(self._tr("xhs_result_empty"))
        self.empty_results.setObjectName("section-hint")
        self.empty_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_results.setMinimumHeight(120)
        v.addWidget(self.empty_results)
        return card

    def _render_templates(self):
        while self.templates_layout.count():
            item = self.templates_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
        self.template_cards = []
        categories = list(dict.fromkeys(t.get("category", "其他") for t in XIAOHONGSHU_TEMPLATES))
        if self.selected_category not in categories:
            self.selected_category = categories[0]

        category_row = QHBoxLayout(); category_row.setContentsMargins(0, 0, 0, 0); category_row.setSpacing(8)
        for category in categories:
            chip = QPushButton(category)
            chip.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            chip.setObjectName("xhs-category-chip-active" if category == self.selected_category else "xhs-category-chip")
            chip.setStyleSheet(self._category_chip_style(category == self.selected_category))
            chip.clicked.connect(lambda checked=False, c=category: self._select_category(c))
            category_row.addWidget(chip)
        category_row.addStretch()
        self.templates_layout.addLayout(category_row)

        host = QWidget(); host.setStyleSheet("background:transparent;")
        grid = QGridLayout(host); grid.setContentsMargins(0, 0, 0, 0); grid.setSpacing(10)
        templates = [t for t in XIAOHONGSHU_TEMPLATES if t.get("category") == self.selected_category]
        for i, template in enumerate(templates):
            card = XiaohongshuTemplateCard(template)
            card.selected.connect(self.apply_template)
            card.activated.connect(self.activate_template)
            self.template_cards.append(card)
            grid.addWidget(card, i // 3, i % 3, Qt.AlignmentFlag.AlignTop)
        for col in range(3):
            grid.setColumnStretch(col, 1)
        self.templates_layout.addWidget(host)

    def _select_category(self, category: str):
        self.selected_category = category
        first = next((t for t in XIAOHONGSHU_TEMPLATES if t.get("category") == category), None)
        if first:
            self.apply_template(first)
        self._render_templates()

    def apply_template(self, template: dict):
        self.selected_template = template
        self.selected_category = template.get("category", self.selected_category)
        if hasattr(self, "selected_label"):
            self.selected_label.setText(f"当前模板：{template.get('title', '')}")
        if hasattr(self, "prompt_edit"):
            self.prompt_edit.setPlainText(template.get("prompt", ""))
        self._set_status(f"已选择模板：{template.get('title', '')}")

    def activate_template(self, template: dict):
        self.apply_template(template)
        self.generate_images()

    def generate_images(self):
        if self._worker:
            return
        prompt = self.prompt_edit.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, self._tr("dialog_tip"), self._tr("need_prompt")); return
        if not self.cfg.get("api_key"):
            QMessageBox.warning(self, self._tr("dialog_tip"), self._tr("need_key")); return

        self.cfg = load_config()
        model = self.cfg.get("model", "gpt-image-2")
        size = compute_size("竖版 3:4", "2K" if model == "gpt-image-2" else "1.5K", model)
        quality = self.cfg.get("default_quality", "auto")
        fmt = self.cfg.get("default_format", "png")
        self._set_generating(True)
        self._set_status(self._tr("requesting"))
        self._worker = GenerateThread(
            self.cfg, prompt, 1, size, quality, fmt, "auto",
            [], False, None, self
        )
        self._worker.finished.connect(lambda paths: self._on_done(paths, prompt, size, quality))
        self._worker.error.connect(self._on_error)
        self._worker.progress.connect(self._set_status)
        self._worker.start()

    def _on_done(self, paths: list, prompt: str, size: str, quality: str):
        self._worker = None
        self._set_generating(False)
        now = datetime.now().isoformat(timespec="seconds")
        title = self.selected_template.get("title", "小红书图文")
        self.session = {
            "id": f"xhs-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "title": f"小红书：{title}",
            "created": now,
            "updated": now,
            "model": self.cfg.get("model", "gpt-image-2"),
            "mode": XHS_MODE,
            "xhs_version": 2,
            "xhs": {
                "template": {
                    "title": self.selected_template.get("title", ""),
                    "category": self.selected_template.get("category", ""),
                    "tags": self.selected_template.get("tags", []),
                },
                "pages": [{"page_no": i + 1, "kind": "image", "final_image": path, "status": "done"} for i, path in enumerate(paths)],
            },
            "turns": [{
                "type": "xhs_template_images",
                "prompt": prompt,
                "model": self.cfg.get("model", "gpt-image-2"),
                "size": size,
                "quality": quality,
                "background": "auto",
                "images": paths,
                "timestamp": now,
            }],
        }
        save_session(self.session)
        self._render_results(paths)
        self._notify_sessions_changed()
        self._set_status(self._tr("done_count").format(count=len(paths)))

    def _on_error(self, msg: str):
        self._worker = None
        self._set_generating(False)
        self._set_status(self._tr("failed"))
        QMessageBox.critical(self, self._tr("failed"), str(msg))

    def _render_results(self, paths: list[str]):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.empty_results.setVisible(not bool(paths))
        existing = [p for p in paths if os.path.exists(p)]
        for i, path in enumerate(existing):
            img = ImageCard(path, i, self)
            img.preview_requested.connect(lambda idx, paths=existing: self._preview(paths, idx))
            img.edit_requested.connect(self._edit_image)
            self.results_layout.addWidget(img, i // 3, i % 3)

    def _set_generating(self, generating: bool):
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText(self._tr("generating") if generating else self._tr("xhs_generate_images"))
        self._style_generate_button(generating)
        self.prompt_edit.setEnabled(not generating)
        for card in self.template_cards:
            card.setEnabled(not generating)

    def _style_generate_button(self, generating: bool):
        self.generate_btn.setStyleSheet(
            "QPushButton {"
            "background:#e11d48; border:none; border-radius:14px; color:#ffffff;"
            "font-size:13px; font-weight:900; padding:10px 26px; min-width:150px;"
            "}"
            "QPushButton:hover { background:#be123c; }"
            if not generating else
            "QPushButton {"
            "background:#e11d48; border:none; border-radius:14px; color:#ffffff;"
            "font-size:13px; font-weight:900; padding:10px 26px; min-width:150px;"
            "}"
        )

    def _category_chip_style(self, active: bool) -> str:
        if active:
            return (
                "QPushButton { background:#fff1f2; border:1px solid #fb7185; color:#be123c;"
                "border-radius:12px; font-size:11px; font-weight:800; padding:6px 10px; }"
            )
        return (
            "QPushButton { background:#ffffff; border:1px solid #e5e7eb; color:#be123c;"
            "border-radius:12px; font-size:11px; font-weight:800; padding:6px 10px; }"
            "QPushButton:hover { background:#fff1f2; border-color:#fb7185; color:#be123c; }"
        )

    def _preview(self, paths: list, index: int):
        if self._on_preview:
            self._on_preview(paths, index)

    def _edit_image(self, image_path: str):
        if self.parent_window and hasattr(self.parent_window, "_start_edit"):
            self.parent_window._switch_page("generate")
            self.parent_window._start_edit(image_path)

    def _notify_sessions_changed(self):
        if self._on_sessions_changed:
            self._on_sessions_changed()

    def _set_status(self, text: str):
        if self.parent_window and hasattr(self.parent_window, "status_bar"):
            self.parent_window.status_bar.showMessage(text, 4000)

    def load_session(self, session: dict):
        self.session = session
        self.cfg = load_config()
        xhs = session.get("xhs", {})
        template = xhs.get("template", {})
        title = template.get("title", "")
        for item in XIAOHONGSHU_TEMPLATES:
            if item.get("title") == title:
                self.apply_template(item)
                self._render_templates()
                break
        turns = session.get("turns", [])
        if turns:
            self.prompt_edit.setPlainText(turns[-1].get("prompt", ""))
            self._render_results(turns[-1].get("images", []))

    def reset(self):
        self.session = None
        self.apply_template(XIAOHONGSHU_TEMPLATES[0])
        self._render_results([])
