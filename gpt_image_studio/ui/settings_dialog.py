import openai

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
)

from ..i18n import I18N
from ..models import MODELS


class SettingsDialog(QDialog):
    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self._tr = getattr(parent, "tr", lambda key: I18N["zh"].get(key, key))
        self.cfg = cfg.copy()
        self.theme = getattr(parent, "theme", cfg.get("theme", "dark"))
        self.setWindowTitle(self._tr("settings_title")); self.setMinimumWidth(480)
        self._apply_theme()

        v = QVBoxLayout(self); v.setContentsMargins(24,22,24,20); v.setSpacing(14)
        t = QLabel(self._tr("settings_title")); t.setObjectName("settings-title")
        v.addWidget(t)

        form = QFormLayout(); form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.key_edit = QLineEdit(cfg.get("api_key",""))
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("sk-…")
        form.addRow("API Key:", self.key_edit)
        self.url_edit = QLineEdit(cfg.get("base_url","https://api.openai.com/v1"))
        form.addRow("Base URL:", self.url_edit)
        self.model_combo = QComboBox(); self.model_combo.addItems(MODELS)
        idx = self.model_combo.findText(cfg.get("model","gpt-image-2"))
        if idx >= 0: self.model_combo.setCurrentIndex(idx)
        form.addRow(self._tr("default_model"), self.model_combo)
        v.addLayout(form)

        hint = QLabel(self._tr("settings_hint"))
        hint.setObjectName("settings-hint"); hint.setWordWrap(True)
        v.addWidget(hint)

        self._test_lbl = QLabel(""); self._test_lbl.setWordWrap(True)
        self._test_lbl.setStyleSheet("font-size:12px;color:#888;min-height:18px;")
        v.addWidget(self._test_lbl)

        br = QHBoxLayout()
        test_btn = QPushButton(self._tr("test_connection"))
        test_btn.clicked.connect(self._test)
        br.addWidget(test_btn); br.addStretch()
        cancel = QPushButton(self._tr("cancel")); cancel.clicked.connect(self.reject)
        save = QPushButton(self._tr("save")); save.setObjectName("save-btn"); save.clicked.connect(self._save)
        br.addWidget(cancel); br.addWidget(save); v.addLayout(br)

    def _apply_theme(self):
        dark = self.theme != "light"
        bg = "#181818" if dark else "#ffffff"
        fg = "#bbbbbb" if dark else "#334155"
        title = "#ffffff" if dark else "#111827"
        field_bg = "#222222" if dark else "#f8fafc"
        border = "#2e2e2e" if dark else "#dbe2ea"
        hover = "#2a2a2a" if dark else "#eef2ff"
        view_bg = "#222222" if dark else "#ffffff"
        hint = "#666666" if dark else "#64748b"
        self.setStyleSheet(f"""
            QDialog{{background:{bg};}}
            QLabel{{color:{fg};font-size:13px;}}
            #settings-title{{color:{title};font-size:16px;font-weight:bold;}}
            #settings-hint{{color:{hint};font-size:11px;}}
            QLineEdit,QComboBox{{background:{field_bg};border:1px solid {border};border-radius:7px;
                color:{title};padding:7px 10px;font-size:13px;}}
            QLineEdit:focus,QComboBox:focus{{border-color:#7c3aed;}}
            QComboBox::drop-down{{border:none;width:18px;}}
            QComboBox QAbstractItemView{{background:{view_bg};color:{title};
                border:1px solid {border};selection-background-color:#ede9fe;}}
            QPushButton{{background:{field_bg};border:1px solid {border};border-radius:7px;
                color:{fg};padding:7px 18px;font-size:13px;}}
            QPushButton:hover{{background:{hover};color:{title};}}
            #save-btn{{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7b2ff7,stop:1 #00b4d8);
                border:none;color:#fff;font-weight:bold;}}
            #save-btn:hover{{
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #9040ff,stop:1 #00c8f0);}}
        """)

    def _test(self):
        key = self.key_edit.text().strip()
        url = self.url_edit.text().strip().rstrip("/")
        if not key:
            self._test_lbl.setStyleSheet("color:#cc6644;font-size:12px;")
            self._test_lbl.setText(self._tr("missing_key")); return
        self._test_lbl.setStyleSheet("color:#888;font-size:12px;")
        self._test_lbl.setText(self._tr("testing")); QApplication.processEvents()
        try:
            client = openai.OpenAI(api_key=key, base_url=url)
            resp = client.images.generate(
                model=self.model_combo.currentText(),
                prompt="a white circle on black background",
                n=1, size="1024x1024", quality="low",
            )
            if resp.data:
                self._test_lbl.setStyleSheet("color:#44bb66;font-size:12px;")
                self._test_lbl.setText(self._tr("test_success"))
            else:
                self._test_lbl.setStyleSheet("color:#cc6644;font-size:12px;")
                self._test_lbl.setText(self._tr("test_no_data"))
        except Exception as e:
            self._test_lbl.setStyleSheet("color:#cc4444;font-size:12px;")
            self._test_lbl.setText(self._tr("test_error").format(error=str(e)[:200]))

    def _save(self):
        self.cfg["api_key"]  = self.key_edit.text().strip()
        self.cfg["base_url"] = self.url_edit.text().strip().rstrip("/")
        self.cfg["model"]    = self.model_combo.currentText()
        self.accept()

    def get_config(self): return self.cfg
