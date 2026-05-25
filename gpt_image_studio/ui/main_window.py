import os
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QKeySequence, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFileDialog, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSpinBox, QSplitter, QStackedWidget, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget,
)

from ..config import load_config, save_config
from ..i18n import I18N
from ..image_utils import crop_square
from ..logging_config import log
from ..models import (
    ASPECT_RATIOS, BACKGROUND_OPTIONS, FORMAT_OPTIONS, MODELS, QUALITY_OPTIONS,
    RESOLUTIONS, RESOLUTIONS_LIMITED, TRANSPARENT_MODELS, compute_size,
)
from ..paths import IMAGES_DIR, LOGO_PATH, SESSIONS_DIR
from ..sessions import list_sessions, load_session, new_session, save_session
from ..styles import THEME_STYLES, apply_app_palette
from ..templates import TEMPLATES
from ..workers.generate_thread import GenerateThread
from .image_widgets import DropZone, TurnWidget
from .preview_dialog import PreviewDialog
from .session_widgets import SessionItem
from .settings_dialog import SettingsDialog
from .template_widgets import TemplateCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg           = load_config()
        self.lang          = self.cfg.get("language", "zh")
        self.theme         = self.cfg.get("theme", "dark")
        self.input_images: list[str] = []
        self._worker       = None
        self._session      = new_session()   # 当前对话
        self._session["model"] = self.cfg.get("model","gpt-image-2")

        self.setWindowTitle("GPT-Image Studio")
        if LOGO_PATH.exists():
            self.setWindowIcon(QIcon(str(LOGO_PATH)))
        self.setMinimumSize(1120, 740); self.resize(1380, 880)
        self._apply_theme_stylesheet()

        self._build_ui()
        self._load_sessions_list()
        self._apply_default_options()
        self._update_res_options()
        self._update_size_preview()
        # 初始化 bg_combo 启用状态（build_ui 完成后才能访问）
        self._on_model_changed(self.cfg.get("model", "gpt-image-2"))

        if not self.cfg.get("api_key"):
            QTimer.singleShot(400, self._open_settings)

    def tr(self, key: str) -> str:
        return I18N.get(self.lang, I18N["zh"]).get(key, key)

    def _apply_theme_stylesheet(self):
        app = QApplication.instance()
        if app is not None:
            apply_app_palette(app, self.theme)
        self.setStyleSheet(THEME_STYLES.get(self.theme, THEME_STYLES["dark"]))

    def _theme_button_text(self) -> str:
        return self.tr("theme_light") if self.theme == "dark" else self.tr("theme_dark")

    # ════════════════ BUILD UI ════════════════
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("app-splitter")
        splitter.setHandleWidth(5)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self._mk_sidebar())
        splitter.addWidget(self._mk_main())
        splitter.setSizes([330, 1050])
        root.addWidget(splitter)

        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.tr("ready"))
        self.prog = QProgressBar()
        self.prog.setRange(0,0); self.prog.setFixedWidth(140)
        self.prog.setFixedHeight(3); self.prog.setVisible(False)
        self.status_bar.addPermanentWidget(self.prog)

    # ── 侧边栏 ─────────────────────────────────
    def _mk_sidebar(self):
        w = QWidget(); w.setObjectName("sidebar"); w.setMinimumWidth(260); w.setMaximumWidth(520)
        v = QVBoxLayout(w); v.setContentsMargins(0,0,0,0); v.setSpacing(0)

        brand = QWidget()
        br = QHBoxLayout(brand); br.setContentsMargins(14,16,14,12); br.setSpacing(10)
        logo = QLabel(); logo.setObjectName("logo-box"); logo.setFixedSize(44,44)
        if LOGO_PATH.exists():
            logo.setPixmap(crop_square(QPixmap(str(LOGO_PATH)), 44))
        br.addWidget(logo)
        bc = QVBoxLayout(); bc.setSpacing(2); bc.setContentsMargins(0,0,0,0)
        title = QLabel("GPT-Image Studio"); title.setObjectName("brand-title")
        sub = QLabel("Local image workspace"); sub.setObjectName("brand-subtitle")
        bc.addWidget(title); bc.addWidget(sub); br.addLayout(bc, 1)
        v.addWidget(brand)

        self.new_btn = QPushButton(self.tr("new"))
        self.new_btn.setObjectName("new-session-btn")
        self.new_btn.clicked.connect(self._new_session)
        v.addWidget(self.new_btn)

        self._page_tabs = {}
        for label, key in [(self.tr("generate_tab"), "generate"), (self.tr("templates_tab"), "templates")]:
            btn = QPushButton(label)
            btn.setObjectName("sidebar-tab-active" if key == "generate" else "sidebar-tab")
            btn.clicked.connect(lambda _, k=key: self._switch_page(k))
            v.addWidget(btn)
            self._page_tabs[key] = btn

        sh = QHBoxLayout(); sh.setContentsMargins(16,12,12,6)
        self.history_label = QLabel(self.tr("history")); self.history_label.setObjectName("section-title")
        sh.addWidget(self.history_label); sh.addStretch()
        self.clear_btn = QPushButton(self.tr("clear"))
        self.clear_btn.setObjectName("clear-history-btn")
        clr = self.clear_btn
        clr.clicked.connect(self._clear_sessions)
        sh.addWidget(clr)
        v.addLayout(sh)

        scroll = QScrollArea(); scroll.setObjectName("session-scroll"); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._sess_container = QWidget(); self._sess_container.setObjectName("session-container")
        self._sess_layout = QVBoxLayout(self._sess_container)
        self._sess_layout.setContentsMargins(0,0,0,0)
        self._sess_layout.setSpacing(4)
        self._sess_layout.addStretch()
        scroll.setWidget(self._sess_container)
        v.addWidget(scroll, 1)

        self.settings_btn = QPushButton(self.tr("settings")); self.settings_btn.setObjectName("sidebar-footer-btn")
        self.settings_btn.clicked.connect(self._open_settings); v.addWidget(self.settings_btn)
        self.folder_btn = QPushButton(self.tr("folder")); self.folder_btn.setObjectName("sidebar-footer-btn")
        self.folder_btn.clicked.connect(lambda: __import__("subprocess").Popen(["explorer", str(IMAGES_DIR)])); v.addWidget(self.folder_btn)
        v.addSpacing(10)
        return w

    # ── 主对话区 ────────────────────────────────
    def _mk_main(self):
        root = QWidget()
        root_layout = QVBoxLayout(root); root_layout.setContentsMargins(0,0,0,0); root_layout.setSpacing(0)
        self.page_stack = QStackedWidget()
        root_layout.addWidget(self.page_stack)

        self.generate_page = QWidget()
        v = QVBoxLayout(self.generate_page); v.setContentsMargins(26,22,26,16); v.setSpacing(16)

        h = QHBoxLayout()
        self.main_title = QLabel(self.tr("main_title"))
        self.main_title.setObjectName("page-title")
        h.addWidget(self.main_title)
        self._session_title_lbl = QLabel(self.tr("new_title"))
        self._session_title_lbl.setObjectName("session-title-pill")
        h.addWidget(self._session_title_lbl)
        h.addStretch()
        self._add_header_actions(h)
        v.addLayout(h)

        card = QFrame(); card.setObjectName("prompt-card")
        cv = QVBoxLayout(card); cv.setContentsMargins(16,14,16,14); cv.setSpacing(12)

        self.prompt_input = QTextEdit()
        self.prompt_input.setObjectName("prompt-input")
        self.prompt_input.setPlaceholderText(self.tr("prompt"))
        self.prompt_input.setMinimumHeight(88); self.prompt_input.setMaximumHeight(150)
        cv.addWidget(self.prompt_input)

        self.drop_zone = DropZone(self)
        self.drop_zone.images_changed.connect(lambda p: setattr(self,"input_images",p))
        cv.addWidget(self.drop_zone)

        # 参数行
        params = QHBoxLayout(); params.setSpacing(6); params.setContentsMargins(2,0,2,0)

        def mk_pill(lbl_text, widget, mw=0):
            pill = QFrame()
            pill.setObjectName("param-pill")
            ph = QHBoxLayout(pill); ph.setContentsMargins(10,0,8,0); ph.setSpacing(6)
            ll = QLabel(lbl_text)
            ll.setObjectName("param-label")
            ph.addWidget(ll)
            widget.setObjectName("param-control")
            if mw: widget.setMinimumWidth(mw)
            ph.addWidget(widget); pill.setFixedHeight(36)
            return pill

        self.model_combo = QComboBox(); self.model_combo.addItems(MODELS)
        idx = self.model_combo.findText(self.cfg.get("model","gpt-image-2"))
        if idx>=0: self.model_combo.setCurrentIndex(idx)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        self.model_pill = mk_pill(self.tr("model"), self.model_combo, 118)
        params.addWidget(self.model_pill)

        # 宽高比
        self.aspect_combo = QComboBox()
        for label in ASPECT_RATIOS: self.aspect_combo.addItem(label)
        self.aspect_combo.setCurrentText("方形 1:1")
        self.aspect_combo.currentTextChanged.connect(self._on_aspect_or_res_changed)
        self.aspect_pill = mk_pill(self.tr("aspect"), self.aspect_combo, 126)
        params.addWidget(self.aspect_pill)

        # 分辨率档位
        self.res_combo = QComboBox()
        self.res_combo.currentTextChanged.connect(self._on_aspect_or_res_changed)
        self.res_pill = mk_pill(self.tr("resolution"), self.res_combo, 50)
        params.addWidget(self.res_pill)

        # 实际 size 预览标签
        self.size_preview = QLabel("1024×1024")
        self.size_preview.setObjectName("size-preview")

        self.quality_combo = QComboBox(); self.quality_combo.addItems(QUALITY_OPTIONS)
        self.quality_combo.setCurrentText(self.cfg.get("default_quality", "auto"))
        self.quality_pill = mk_pill(self.tr("quality"), self.quality_combo, 64)
        params.addWidget(self.quality_pill)

        self.fmt_combo = QComboBox(); self.fmt_combo.addItems(FORMAT_OPTIONS)
        self.fmt_combo.setCurrentText(self.cfg.get("default_format", "png"))
        self.format_pill = mk_pill(self.tr("format"), self.fmt_combo, 56)
        params.addWidget(self.format_pill)

        self.bg_combo = QComboBox(); self.bg_combo.addItems(BACKGROUND_OPTIONS)
        self.bg_combo.currentTextChanged.connect(self._on_bg_changed)
        self.bg_combo.setCurrentText("auto")
        self.n_spin = QSpinBox(); self.n_spin.setRange(1,10); self.n_spin.setValue(1)
        self.thinking_btn = QPushButton("Thinking")
        self.thinking_btn.setCheckable(True)
        self.thinking_btn.setVisible(False)

        params.addStretch()

        self.gen_btn = QPushButton(self.tr("generate")); self.gen_btn.setObjectName("gen-btn")
        self.gen_btn.setFixedHeight(42); self.gen_btn.setMinimumWidth(150)
        self.gen_btn.clicked.connect(self._generate)
        self.gen_btn.setShortcut(QKeySequence("Ctrl+Return"))
        params.addWidget(self.gen_btn)
        cv.addLayout(params)
        v.addWidget(card)

        self.gen_content_stack = QStackedWidget()
        self._template_areas = []
        self.gen_templates_view = self._mk_templates_area(self.tr("template_title"), self.tr("template_hint"))
        self.results_page = self._mk_results_area()
        self.gen_content_stack.addWidget(self.gen_templates_view)
        self.gen_content_stack.addWidget(self.results_page)
        self.gen_content_stack.setCurrentWidget(self.gen_templates_view)

        v.addWidget(self.gen_content_stack, 1)

        self.templates_page = QWidget()
        tv = QVBoxLayout(self.templates_page); tv.setContentsMargins(26,22,26,16); tv.setSpacing(16)
        th = QHBoxLayout()
        self.templates_page_title = QLabel(self.tr("templates_tab"))
        tt = self.templates_page_title
        tt.setObjectName("page-title")
        th.addWidget(tt); th.addStretch(); self._add_header_actions(th, secondary=True); tv.addLayout(th)
        tv.addWidget(self._mk_templates_area(self.tr("template_library"), self.tr("template_library_hint")), 1)

        self.page_stack.addWidget(self.generate_page)
        self.page_stack.addWidget(self.templates_page)
        self.page_stack.setCurrentWidget(self.generate_page)
        return root

    def _add_header_actions(self, layout, secondary: bool = False):
        lang_btn = QPushButton(self.tr("language"))
        lang_btn.setObjectName("header-action-btn")
        lang_btn.clicked.connect(self._toggle_language)
        layout.addWidget(lang_btn)
        theme_btn = QPushButton(self._theme_button_text())
        theme_btn.setObjectName("header-action-btn")
        theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(theme_btn)
        if not secondary:
            self.lang_btn = lang_btn
            self.theme_btn = theme_btn
        else:
            self.templates_lang_btn = lang_btn
            self.templates_theme_btn = theme_btn

    def _mk_templates_area(self, title_text="灵感模板", hint_text="点击模板会填入提示词"):
        w = QWidget()
        v = QVBoxLayout(w); v.setContentsMargins(0,0,0,0); v.setSpacing(10)
        h = QHBoxLayout()
        t = QLabel(title_text)
        t.setObjectName("section-heading")
        h.addWidget(t)
        hint = QLabel(hint_text)
        hint.setObjectName("section-hint")
        h.addWidget(hint); h.addStretch(); v.addLayout(h)
        if hasattr(self, "_template_areas"):
            self._template_areas.append((t, hint))

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")
        body = QWidget(); body.setStyleSheet("background:transparent;")
        grid = QGridLayout(body); grid.setContentsMargins(0,0,0,0); grid.setSpacing(12)
        for i, template in enumerate(TEMPLATES):
            card = TemplateCard(template)
            card.selected.connect(self._apply_template)
            grid.addWidget(card, i // 3, i % 3)
        grid.setRowStretch((len(TEMPLATES) + 2) // 3, 1)
        scroll.setWidget(body)
        v.addWidget(scroll, 1)
        return w

    def _mk_results_area(self):
        w = QFrame(); w.setObjectName("result-card")
        v = QVBoxLayout(w); v.setContentsMargins(14,14,14,14); v.setSpacing(10)
        h = QHBoxLayout()
        self.current_title = QLabel(self.tr("current"))
        self.current_title.setObjectName("section-heading")
        h.addWidget(self.current_title)
        self._result_hint = QLabel(self.tr("current_hint"))
        self._result_hint.setObjectName("section-hint")
        h.addWidget(self._result_hint); h.addStretch(); v.addLayout(h)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background:transparent;")
        self._chat_layout = QVBoxLayout(self.chat_container)
        self._chat_layout.setContentsMargins(0,0,0,0)
        self._chat_layout.setSpacing(10)
        self._chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_container)
        v.addWidget(self.chat_scroll, 1)
        return w

    # ════════════════ LOGIC ════════════════
    def _nav(self, key):
        pass

    def _apply_default_options(self):
        self.model_combo.setCurrentText(self.cfg.get("model", "gpt-image-2"))
        self.aspect_combo.setCurrentText(self.cfg.get("default_aspect", "方形 1:1"))
        self.res_combo.setCurrentText(self.cfg.get("default_resolution", "2K"))
        self.quality_combo.setCurrentText(self.cfg.get("default_quality", "auto"))
        self.fmt_combo.setCurrentText(self.cfg.get("default_format", "png"))

    def _switch_page(self, key: str):
        if not hasattr(self, "page_stack"):
            return
        target = self.templates_page if key == "templates" else self.generate_page
        self.page_stack.setCurrentWidget(target)
        for tab_key, btn in self._page_tabs.items():
            btn.setObjectName("sidebar-tab-active" if tab_key == key else "sidebar-tab")
            btn.style().unpolish(btn); btn.style().polish(btn)

    def _on_model_changed(self, model: str):
        self.cfg["model"] = model
        self._session["model"] = model
        self._update_res_options()
        self._update_size_preview()
        self.thinking_btn.setEnabled(model == "gpt-image-2")
        if model != "gpt-image-2": self.thinking_btn.setChecked(False)
        # 透明背景只有 gpt-image-1/1.5 支持
        supports_bg = model in TRANSPARENT_MODELS
        self.bg_combo.setEnabled(supports_bg)
        if not supports_bg and self.bg_combo.currentText() == "transparent":
            self.bg_combo.setCurrentIndex(0)  # 重置为 auto

    def _on_bg_changed(self, val: str):
        """背景选择变化时，透明模式自动切换格式到 png"""
        if not hasattr(self, "fmt_combo"): return
        if val == "transparent":
            if self.fmt_combo.currentText() == "jpeg":
                self.fmt_combo.setCurrentText("png")
            # 禁用 jpeg 选项
            for i in range(self.fmt_combo.count()):
                if self.fmt_combo.itemText(i) == "jpeg":
                    # 不能直接 disable item，用颜色提示
                    pass
        log.debug(f"[BG] background={val}, fmt={self.fmt_combo.currentText()}")

    def _on_aspect_or_res_changed(self):
        self._update_size_preview()

    def _update_res_options(self):
        """根据模型填充分辨率档位"""
        model = self.model_combo.currentText() if hasattr(self, "model_combo") else "gpt-image-2"
        cur = self.res_combo.currentText() if hasattr(self, "res_combo") else ""
        self.res_combo.blockSignals(True)
        self.res_combo.clear()
        res_map = RESOLUTIONS if model == "gpt-image-2" else RESOLUTIONS_LIMITED
        for label in res_map:
            self.res_combo.addItem(label)
        idx = self.res_combo.findText(cur)
        if idx < 0:
            default_res = self.cfg.get("default_resolution", "2K")
            idx = self.res_combo.findText(default_res)
        if idx >= 0:
            self.res_combo.setCurrentIndex(idx)
        self.res_combo.blockSignals(False)
        self._update_size_preview()

    def _update_size_options(self):
        # 兼容旧调用路径
        self._update_res_options()
        self._update_size_preview()

    def _update_size_preview(self):
        """更新 size 预览标签"""
        if not hasattr(self, "aspect_combo") or not hasattr(self, "res_combo"):
            return
        model  = self.model_combo.currentText()
        aspect = self.aspect_combo.currentText()
        res    = self.res_combo.currentText()
        size   = compute_size(aspect, res, model)
        if size == "auto":
            self.size_preview.setText("auto")
        else:
            w, h = size.split("x")
            self.size_preview.setText(f"{w}×{h}")
        log.debug(f"[SIZE PREVIEW] aspect={aspect!r} res={res!r} model={model} -> {size}")

    def _on_tag(self):
        active = [b.text() for b in self._tag_btns if b.isChecked()]
        if not active: return
        cur = self.prompt_input.toPlainText().strip()
        style_str = "，".join(active) + " 风格"
        if style_str not in cur:
            self.prompt_input.setPlainText((cur+"，" if cur else "") + style_str)

    def _apply_template(self, prompt: str):
        self.prompt_input.setPlainText(prompt)
        self.prompt_input.setFocus()
        self.status_bar.showMessage("已填入模板提示词" if self.lang == "zh" else "Template prompt applied", 2500)

    def _show_results_page(self):
        self._switch_page("generate")
        if hasattr(self, "gen_content_stack"):
            self.gen_content_stack.setCurrentWidget(self.results_page)

    def _show_generation_templates(self):
        self._switch_page("generate")
        if hasattr(self, "gen_content_stack"):
            self.gen_content_stack.setCurrentWidget(self.gen_templates_view)

    def _collect_generation_params(self) -> dict:
        model = self.model_combo.currentText()
        aspect = self.aspect_combo.currentText()
        res = self.res_combo.currentText()
        size = compute_size(aspect, res, model)
        return {
            "model": model,
            "aspect": aspect,
            "resolution": res,
            "size": size,
            "quality": self.quality_combo.currentText(),
            "format": self.fmt_combo.currentText(),
            "background": self.bg_combo.currentText(),
            "n": self.n_spin.value(),
            "thinking": self.thinking_btn.isChecked(),
        }

    def _toggle_language(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self.cfg["language"] = self.lang
        save_config(self.cfg)
        self._refresh_language()

    def _toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.cfg["theme"] = self.theme
        save_config(self.cfg)
        self._apply_theme_stylesheet()
        self.drop_zone.apply_theme()
        self._rebuild_chat_area()
        self._load_sessions_list()
        self._refresh_theme_buttons()

    def _refresh_theme_buttons(self):
        if hasattr(self, "theme_btn"):
            self.theme_btn.setText(self._theme_button_text())
        if hasattr(self, "templates_theme_btn"):
            self.templates_theme_btn.setText(self._theme_button_text())

    def _refresh_language(self):
        self.new_btn.setText(self.tr("new"))
        self._page_tabs["generate"].setText(self.tr("generate_tab"))
        self._page_tabs["templates"].setText(self.tr("templates_tab"))
        self.history_label.setText(self.tr("history"))
        self.clear_btn.setText(self.tr("clear"))
        self.settings_btn.setText(self.tr("settings"))
        self.folder_btn.setText(self.tr("folder"))
        self.lang_btn.setText(self.tr("language"))
        self.templates_lang_btn.setText(self.tr("language"))
        self._refresh_theme_buttons()
        self.main_title.setText(self.tr("main_title"))
        if not self._session.get("turns"):
            self._session_title_lbl.setText(self.tr("new_title"))
        self.prompt_input.setPlaceholderText(self.tr("prompt"))
        self.drop_zone._hint.setText(self.tr("drop_hint"))
        self.drop_zone.add_btn.setText(self.tr("add_image"))
        self.gen_btn.setText(self.tr("generate"))
        if hasattr(self, "templates_page_title"):
            self.templates_page_title.setText(self.tr("templates_tab"))
        if hasattr(self, "_template_areas") and len(self._template_areas) >= 2:
            self._template_areas[0][0].setText(self.tr("template_title"))
            self._template_areas[0][1].setText(self.tr("template_hint"))
            self._template_areas[1][0].setText(self.tr("template_library"))
            self._template_areas[1][1].setText(self.tr("template_library_hint"))
        if hasattr(self, "current_title"):
            self.current_title.setText(self.tr("current"))
            self._result_hint.setText(self.tr("current_hint"))
        self.status_bar.showMessage(self.tr("ready"), 2000)

    def _open_settings(self):
        dlg = SettingsDialog(self.cfg, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.cfg = dlg.get_config(); save_config(self.cfg)
            idx = self.model_combo.findText(self.cfg["model"])
            if idx>=0: self.model_combo.setCurrentIndex(idx)
            self.status_bar.showMessage(self.tr("settings_saved"), 3000)

    def _generate(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, self.tr("dialog_tip"), self.tr("need_prompt")); return
        if not self.cfg.get("api_key"):
            QMessageBox.warning(self, self.tr("dialog_tip"), self.tr("need_key")); self._open_settings(); return

        ui_params  = self._collect_generation_params()
        model      = ui_params["model"]
        aspect     = ui_params["aspect"]
        res        = ui_params["resolution"]
        size       = ui_params["size"]
        quality    = ui_params["quality"]
        fmt        = ui_params["format"]
        background = ui_params["background"]
        n          = ui_params["n"]
        thinking   = ui_params["thinking"]
        log.info(f"[UI PARAMS] {ui_params}")

        # 透明背景：只有 gpt-image-1/1.5 支持
        if background == "transparent" and model not in TRANSPARENT_MODELS:
            QMessageBox.warning(
                self, self.tr("unsupported"),
                self.tr("transparent_not_supported").format(model=model)
            )
            return

        # 透明背景不能用 jpeg
        if background == "transparent" and fmt == "jpeg":
            fmt = "png"
            log.warning("[UI] transparent 强制切换 fmt -> png")

        ctx_img = None
        is_edit_mode = bool(self.input_images)
        if not is_edit_mode:
            self._session = new_session()
            self._session["model"] = model
            self._session_title_lbl.setText(self.tr("new_title"))
            self._clear_chat_area()
        else:
            log.info(f"[EDIT MODE] 使用参考图继续当前历史: {self.input_images[0]}")
        self._show_results_page()

        self.gen_btn.setEnabled(False); self.gen_btn.setText(self.tr("generating"))
        self.prog.setVisible(True); self.status_bar.showMessage(self.tr("requesting"))

        self._worker = GenerateThread(
            self.cfg, prompt, n, size, quality, fmt, background,
            self.input_images, thinking, ctx_img, self
        )
        self._worker.finished.connect(
            lambda paths: self._on_done(paths, prompt, size, quality, background)
        )
        self._worker.error.connect(self._on_error)
        self._worker.progress.connect(self.status_bar.showMessage)
        self._worker.start()

    def _on_done(self, paths: list, prompt: str, size: str, quality: str, background: str):
        self.gen_btn.setEnabled(True); self.gen_btn.setText(self.tr("generate"))
        self.prog.setVisible(False)
        self.status_bar.showMessage(self.tr("done_count").format(count=len(paths)), 6000)

        turn = {
            "prompt":     prompt,
            "model":      self.cfg.get("model",""),
            "size":       size,
            "quality":    quality,
            "background": background,
            "thinking":   self.thinking_btn.isChecked(),
            "images":     paths,
            "timestamp":  datetime.now().isoformat(timespec="seconds"),
        }
        self._session["turns"].append(turn)
        self._session["updated"] = datetime.now().isoformat(timespec="seconds")

        # 自动用第一条 prompt 作为会话标题
        if len(self._session["turns"]) == 1:
            self._session["title"] = prompt[:30] + ("…" if len(prompt)>30 else "")
            self._session_title_lbl.setText(self._session["title"])

        save_session(self._session)
        self._append_turn_widget(turn)
        self._load_sessions_list()

        # 清空输入图（编辑模式结束后回到普通新生成模式，保持 prompt 不变）
        self.drop_zone.image_paths = []
        self.drop_zone._rebuild()
        self.input_images = []

    def _on_error(self, msg: str):
        self.gen_btn.setEnabled(True); self.gen_btn.setText(self.tr("generate"))
        self.prog.setVisible(False); self.status_bar.showMessage(self.tr("failed"), 4000)
        QMessageBox.critical(self, self.tr("failed"), msg)

    def _append_turn_widget(self, turn: dict):
        """把一轮对话追加到对话区末尾"""
        # 收集当前 session 所有图片（用于预览器翻页）
        all_paths = []
        for t in self._session["turns"]:
            all_paths.extend(p for p in t.get("images",[]) if os.path.exists(p))

        base_idx = len(all_paths) - len([p for p in turn.get("images",[]) if os.path.exists(p)])
        tw = TurnWidget(turn, all_paths, base_idx, self)
        tw.preview_requested.connect(self._open_preview)
        tw.edit_requested.connect(self._start_edit)

        # 插入在 stretch 之前
        self._chat_layout.insertWidget(self._chat_layout.count()-1, tw)
        # 滚动到底部
        QTimer.singleShot(50, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    def _open_preview(self, paths: list, index: int):
        if not paths: return
        dlg = PreviewDialog(paths, index, self)
        dlg.exec()

    def _start_edit(self, image_path: str):
        """把图片填入上传区，让用户输入新 prompt 后以编辑模式生成"""
        if not os.path.exists(image_path): return
        self.drop_zone._add([image_path])
        self.input_images = list(self.drop_zone.image_paths)
        self.prompt_input.setFocus()
        self.prompt_input.selectAll()
        self.status_bar.showMessage(self.tr("edit_selected").format(name=os.path.basename(image_path)), 6000)

    # ── 会话管理 ─────────────────────────────────
    def _new_session(self):
        """保存当前对话，开启新对话"""
        if self._session["turns"]:
            save_session(self._session)
        self._session = new_session()
        self._session["model"] = self.cfg.get("model","gpt-image-2")
        self._session_title_lbl.setText(self.tr("new_title"))
        self._clear_chat_area()
        self._load_sessions_list()
        self.prompt_input.clear()
        self.drop_zone.image_paths = []
        self.drop_zone._rebuild()
        self.input_images = []
        self._show_generation_templates()

    def _clear_chat_area(self):
        while self._chat_layout.count() > 1:
            item = self._chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def _rebuild_chat_area(self):
        if not hasattr(self, "_chat_layout"):
            return
        self._clear_chat_area()
        all_paths = []
        for turn in self._session.get("turns", []):
            all_paths.extend(p for p in turn.get("images", []) if os.path.exists(p))
        offset = 0
        for turn in self._session.get("turns", []):
            imgs = [p for p in turn.get("images", []) if os.path.exists(p)]
            tw = TurnWidget(turn, all_paths, offset, self)
            tw.preview_requested.connect(self._open_preview)
            tw.edit_requested.connect(self._start_edit)
            self._chat_layout.insertWidget(self._chat_layout.count()-1, tw)
            offset += len(imgs)

    def _load_sessions_list(self):
        while self._sess_layout.count() > 1:
            item = self._sess_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for sess in list_sessions():
            active = (sess["id"] == self._session["id"])
            item = SessionItem(sess, active)
            item.clicked_signal.connect(self._switch_session)
            self._sess_layout.insertWidget(self._sess_layout.count()-1, item)

    def _switch_session(self, sid: str):
        if sid == self._session["id"]: return
        if self._session["turns"]: save_session(self._session)
        data = load_session(sid)
        if not data: return
        self._session = data
        self._session_title_lbl.setText(data.get("title", self.tr("new_title")))
        self._clear_chat_area()
        self._show_results_page()

        # 重建对话气泡
        all_paths = []
        for t in data.get("turns",[]):
            all_paths.extend(p for p in t.get("images",[]) if os.path.exists(p))

        offset = 0
        for t in data.get("turns",[]):
            imgs = [p for p in t.get("images",[]) if os.path.exists(p)]
            tw = TurnWidget(t, all_paths, offset, self)
            tw.preview_requested.connect(self._open_preview)
            tw.edit_requested.connect(self._start_edit)
            self._chat_layout.insertWidget(self._chat_layout.count()-1, tw)
            offset += len(imgs)

        self._load_sessions_list()
        QTimer.singleShot(80, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    def _clear_sessions(self):
        if QMessageBox.question(
            self, self.tr("clear_confirm_title"), self.tr("clear_confirm_text"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            for p in SESSIONS_DIR.glob("*.json"): p.unlink()
            self._session = new_session()
            self._session["model"] = self.cfg.get("model","gpt-image-2")
            self._session_title_lbl.setText(self.tr("new_title"))
            self._clear_chat_area()
            self._load_sessions_list()
            self._show_generation_templates()

