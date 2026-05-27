from PyQt6.QtGui import QColor, QPalette


BASE_STYLE = """
* { font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif; }
QPushButton { font-size:13px; }

#gen-btn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7c3aed,stop:1 #2563eb);
    border:none; border-radius:16px; color:#fff;
    font-size:14px; font-weight:bold; padding:8px 24px;
    min-width:96px; min-height:36px;
}
#gen-btn:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8b5cf6,stop:1 #3b82f6);
}
#gen-btn:disabled { background:#283041; color:#64748b; }

#new-session-btn {
    background:#f8fafc; border:none; border-radius:12px; color:#0f172a;
    font-size:12px; font-weight:800; padding:9px 12px; margin:8px 10px;
}
#new-session-btn:hover { background:#dbeafe; }

QProgressBar { border:none; border-radius:2px; height:3px; }
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7b2ff7,stop:1 #00b4d8);
    border-radius:2px;
}
QLineEdit, QComboBox, QSpinBox {
    border-radius:7px; padding:6px 10px; font-size:13px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border-color:#7c3aed; }
#header-action-btn {
    border-radius:12px; font-size:12px; font-weight:700; padding:7px 12px;
}
#clear-history-btn { background:transparent; border:none; color:#64748b; font-size:11px; }
#clear-history-btn:hover { color:#ef4444; }
#page-title { font-size:26px; font-weight:900; }
#section-heading { font-size:15px; font-weight:800; }
#section-hint { font-size:11px; }
#session-title-pill { font-size:12px; border-radius:12px; padding:5px 12px; }
#param-pill { border-radius:14px; }
#param-label { font-size:11px; background:transparent; border:none; }
#param-control {
    background:transparent; border:none; font-size:12px; padding:0 2px; min-height:32px;
}
#param-control::drop-down { border:none; width:14px; }
#param-control::down-arrow { image:none; border:none; }
#param-control::up-button, #param-control::down-button { width:0; border:none; background:transparent; }
#size-preview { font-size:10px; min-width:80px; }
#drop-hint { border-radius:10px; font-size:12px; padding:14px 10px; }
#drop-chip-row { border-radius:10px; }
#card-action-btn { border-radius:5px; font-size:12px; }
#red-bg-btn { border-radius:5px; font-size:11px; }
#image-thumb, #chip-thumb, #session-thumb, #template-image { border-radius:10px; }
#image-thumb[red="true"] { background:#cc2222; }
#template-title { font-size:12px; font-weight:700; background:transparent; }
#template-prompt { font-size:10px; line-height:14px; background:transparent; }
#session-title { font-size:12px; font-weight:600; line-height:16px; }
#session-meta { font-size:10px; }
#turn-prompt { font-size:13px; }
#turn-meta { font-size:11px; }
#xhs-step-card, #xhs-page-card { border-radius:18px; }
#xhs-field-label { font-size:11px; font-weight:700; }
#xhs-page-status { font-size:11px; font-weight:800; border-radius:10px; padding:4px 10px; }
#xhs-primary-btn, #xhs-secondary-btn { border-radius:12px; font-size:12px; font-weight:800; padding:8px 14px; }
#xhs-primary-btn:disabled, #xhs-secondary-btn:disabled { background:#475569; color:#cbd5e1; }
QPushButton#xhs-generate-btn { background:#ff3b5c; border:none; border-radius:14px; color:#ffffff; font-size:13px; font-weight:900; padding:10px 26px; min-width:150px; }
QPushButton#xhs-generate-btn:hover { background:#ff5470; }
QPushButton#xhs-generate-btn:disabled { background:#ff3b5c; color:#ffffff; border:none; }
#xhs-template-btn, #xhs-template-btn-active { border-radius:14px; text-align:left; }
#xhs-template-card { border-radius:14px; }
#xhs-template-preview { border-radius:10px; }
#xhs-category-chip, #xhs-category-chip-active { border-radius:12px; font-size:11px; font-weight:800; padding:6px 10px; }
#preview-canvas { background:#0a0a0a; border:none; }
"""

DARK_STYLE = BASE_STYLE + """
QMainWindow, QWidget { background-color:#0b0d12; color:#e8e8e8; }
#app-splitter::handle { background:#202431; }
#app-splitter::handle:hover { background:#7c3aed; }
#sidebar, #session-scroll, #session-container { background:#0f1117; }
#sidebar { border-right:1px solid #202431; }
#logo-box { background:#151923; border-radius:12px; }
#brand-title { color:#f8fafc; font-size:16px; font-weight:800; }
#brand-subtitle { color:#677084; font-size:10px; }
#section-title { color:#7b8190; font-size:11px; font-weight:700; letter-spacing:1px; }
#sidebar-tab {
    background:#151923; border:1px solid #252b3a; border-radius:12px;
    color:#9ca3af; font-size:13px; font-weight:700; padding:10px 12px; margin:3px 10px; text-align:left;
}
#sidebar-tab:hover { background:#1b2130; color:#f8fafc; border-color:#475569; }
#sidebar-tab-active {
    background:#24143f; border:1px solid #7c3aed; border-radius:12px;
    color:#f8fafc; font-size:13px; font-weight:800; padding:10px 12px; margin:3px 10px; text-align:left;
}
#sidebar-footer-btn {
    background:#151923; border:1px solid #252b3a; border-radius:10px;
    color:#9ca3af; font-size:12px; padding:8px 12px; margin:3px 10px; text-align:left;
}
#sidebar-footer-btn:hover { background:#1b2130; color:#f3f4f6; border-color:#334155; }
#prompt-card, #result-card, #turn-frame, #xhs-step-card { background:#121722; border:1px solid #293144; border-radius:18px; }
#xhs-page-card { background:#111827; border:1px solid #273244; border-radius:16px; }
#xhs-field-label { color:#94a3b8; }
#xhs-page-status { background:#24143f; color:#c4b5fd; }
#xhs-primary-btn { background:#7c3aed; border:none; color:#ffffff; }
#xhs-primary-btn:hover { background:#8b5cf6; }
#xhs-secondary-btn { background:#151923; border:1px solid #252b3a; color:#cbd5e1; }
#xhs-secondary-btn:hover { background:#1b2130; border-color:#7c3aed; color:#f8fafc; }
#xhs-template-btn { background:#151923; border:1px solid #252b3a; color:#cbd5e1; }
#xhs-template-btn:hover { background:#1b2130; border-color:#475569; }
#xhs-template-btn-active { background:#24143f; border:1px solid #7c3aed; color:#f8fafc; }
#xhs-template-card { background:#111827; border:1px solid #273244; }
#xhs-template-card:hover { background:#151c2b; border-color:#ff3b5c; }
#xhs-template-preview { background:#0d111a; }
#xhs-category-chip { background:#151923; border:1px solid #252b3a; color:#cbd5e1; }
#xhs-category-chip:hover { background:#1b2130; border-color:#ff3b5c; color:#ffffff; }
#xhs-category-chip-active { background:#3b1020; border:1px solid #ff3b5c; color:#ffffff; }
QTextEdit#prompt-input {
    background:#0d111a; border:1px solid #252b3a; border-radius:14px; color:#f8fafc;
    font-size:14px; padding:10px 12px; selection-background-color:#4c1d95;
}
QTextEdit#prompt-input:focus { border-color:#7c3aed; }
#session-item { background:#141925; border:1px solid #252b3a; border-radius:14px; margin:2px 8px; }
#session-item:hover { border-color:#475569; background:#192132; }
#session-item-active { background:#211638; border:1px solid #7c3aed; border-radius:14px; margin:2px 8px; }
#img-card, #template-card { background:#111827; border:1px solid #273244; border-radius:16px; }
#img-card:hover { border-color:#475569; }
#template-card:hover { border-color:#7c3aed; background:#151c2b; }
#page-title, #section-heading { color:#f8fafc; }
#section-hint, #param-label, #turn-meta, #session-meta, #template-prompt { color:#64748b; }
#session-title-pill { color:#94a3b8; background:#111827; border:1px solid #273244; }
#param-pill { background:#0d111a; border:1px solid #273244; }
#param-control { color:#e5e7eb; }
#param-control QAbstractItemView { background:#111827; border:1px solid #334155; color:#e5e7eb; selection-background-color:#312e81; outline:none; padding:4px; }
#size-preview { color:#555; }
#drop-hint { background:#111; border:1.5px dashed #2a2a2a; color:#444; }
#drop-hint:hover { border-color:#3d3d3d; color:#666; }
#drop-hint[dragging="true"] { background:#120d22; border-color:#7b2ff7; color:#aa77ff; }
#drop-chip-row { background:#111; border:1.5px solid #1e1e1e; }
#drop-chip-row[dragging="true"] { background:#120d22; border-color:#7b2ff7; }
#card-action-btn, #red-bg-btn { background:#1e1e1e; border:1px solid #2a2a2a; color:#888; }
#card-action-btn:hover { background:#2a2a2a; color:#eee; }
#red-bg-btn:hover { border-color:#883333; color:#ffaaaa; }
#red-bg-btn:checked { background:#2a0a0a; border-color:#cc3333; }
#image-thumb, #chip-thumb, #template-image { background:#111827; }
#session-thumb { background:#202020; color:#555; }
#template-title, #session-title, #turn-prompt { color:#e5e7eb; }
QScrollBar:vertical { background:#0b0d12; width:5px; border-radius:2px; }
QScrollBar::handle:vertical { background:#2e2e2e; border-radius:2px; min-height:24px; }
QScrollBar::handle:vertical:hover { background:#444; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QScrollBar:horizontal { background:#0b0d12; height:5px; border-radius:2px; }
QScrollBar::handle:horizontal { background:#2e2e2e; border-radius:2px; min-width:24px; }
QScrollBar::handle:horizontal:hover { background:#444; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width:0; }
QStatusBar { background:#0f0f0f; color:#555; font-size:11px; border-top:1px solid #1a1a1a; }
QProgressBar { background:#1e1e1e; }
QMessageBox { background:#1a1a1a; color:#e0e0e0; }
QDialog { background:#181818; }
QDialog QLabel { color:#ccc; }
QLineEdit, QComboBox, QSpinBox { background:#222; border:1px solid #2e2e2e; color:#e8e8e8; }
#header-action-btn { background:#151923; border:1px solid #252b3a; color:#cbd5e1; }
#header-action-btn:hover { background:#1b2130; color:#f8fafc; border-color:#7c3aed; }
"""

LIGHT_STYLE = BASE_STYLE + """
QMainWindow, QWidget { background-color:#f6f8fb; color:#111827; }
#app-splitter::handle { background:#dbe2ea; }
#app-splitter::handle:hover { background:#7c3aed; }
#sidebar, #session-scroll, #session-container { background:#ffffff; }
#sidebar { border-right:1px solid #dbe2ea; }
#logo-box { background:#eef2ff; border-radius:12px; }
#brand-title { color:#111827; font-size:16px; font-weight:800; }
#brand-subtitle { color:#64748b; font-size:10px; }
#section-title { color:#64748b; font-size:11px; font-weight:700; letter-spacing:1px; }
#sidebar-tab {
    background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;
    color:#475569; font-size:13px; font-weight:700; padding:10px 12px; margin:3px 10px; text-align:left;
}
#sidebar-tab:hover { background:#eef2ff; color:#111827; border-color:#c7d2fe; }
#sidebar-tab-active {
    background:#ede9fe; border:1px solid #7c3aed; border-radius:12px;
    color:#312e81; font-size:13px; font-weight:800; padding:10px 12px; margin:3px 10px; text-align:left;
}
#sidebar-footer-btn {
    background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px;
    color:#475569; font-size:12px; padding:8px 12px; margin:3px 10px; text-align:left;
}
#sidebar-footer-btn:hover { background:#eef2ff; color:#111827; border-color:#c7d2fe; }
#prompt-card, #result-card, #turn-frame, #xhs-step-card { background:#ffffff; border:1px solid #dbe2ea; border-radius:18px; }
#xhs-page-card { background:#ffffff; border:1px solid #dbe2ea; border-radius:16px; }
#xhs-field-label { color:#64748b; }
#xhs-page-status { background:#ede9fe; color:#5b21b6; }
#xhs-primary-btn { background:#7c3aed; border:none; color:#ffffff; }
#xhs-primary-btn:hover { background:#8b5cf6; }
#xhs-secondary-btn { background:#ffffff; border:1px solid #dbe2ea; color:#475569; }
#xhs-secondary-btn:hover { background:#eef2ff; border-color:#7c3aed; color:#312e81; }
#xhs-template-btn { background:#ffffff; border:1px solid #dbe2ea; color:#475569; }
#xhs-template-btn:hover { background:#f8fafc; border-color:#c7d2fe; }
#xhs-template-btn-active { background:#ede9fe; border:1px solid #7c3aed; color:#312e81; }
#xhs-template-card { background:#ffffff; border:1px solid #dbe2ea; }
#xhs-template-card:hover { background:#fff7f8; border-color:#ff3b5c; }
#xhs-template-preview { background:#f1f5f9; }
#xhs-category-chip { background:#ffffff; border:1px solid #dbe2ea; color:#be123c; }
#xhs-category-chip:hover { background:#fff7f8; border-color:#ff3b5c; color:#9f1239; }
#xhs-category-chip-active { background:#ff3b5c; border:1px solid #ff3b5c; color:#ffffff; }
QTextEdit#prompt-input {
    background:#f8fafc; border:1px solid #dbe2ea; border-radius:14px; color:#111827;
    font-size:14px; padding:10px 12px; selection-background-color:#ddd6fe;
}
QTextEdit#prompt-input:focus { border-color:#7c3aed; }
#session-item { background:#ffffff; border:1px solid #e2e8f0; border-radius:14px; margin:2px 8px; }
#session-item:hover { background:#f8fafc; border-color:#cbd5e1; }
#session-item-active { background:#ede9fe; border:1px solid #7c3aed; border-radius:14px; margin:2px 8px; }
#img-card, #template-card { background:#ffffff; border:1px solid #dbe2ea; border-radius:16px; }
#img-card:hover, #template-card:hover { background:#f8fafc; border-color:#7c3aed; }
#page-title, #section-heading, #template-title, #session-title, #turn-prompt { color:#111827; }
#section-hint, #param-label, #turn-meta, #session-meta, #template-prompt { color:#64748b; }
#session-title-pill { color:#475569; background:#ffffff; border:1px solid #dbe2ea; }
#param-pill { background:#f8fafc; border:1px solid #dbe2ea; }
#param-control { color:#111827; }
#param-control QAbstractItemView { background:#ffffff; border:1px solid #cbd5e1; color:#111827; selection-background-color:#ede9fe; outline:none; padding:4px; }
#size-preview { color:#64748b; }
#drop-hint { background:#ffffff; border:1.5px dashed #cbd5e1; color:#64748b; }
#drop-hint:hover { border-color:#a78bfa; color:#312e81; }
#drop-hint[dragging="true"] { background:#f5f3ff; border-color:#7c3aed; color:#6d28d9; }
#drop-chip-row { background:#ffffff; border:1.5px solid #dbe2ea; }
#drop-chip-row[dragging="true"] { background:#f5f3ff; border-color:#7c3aed; }
#card-action-btn, #red-bg-btn { background:#f8fafc; border:1px solid #dbe2ea; color:#475569; }
#card-action-btn:hover { background:#eef2ff; color:#111827; }
#red-bg-btn:hover { border-color:#fca5a5; color:#b91c1c; }
#red-bg-btn:checked { background:#fee2e2; border-color:#ef4444; color:#991b1b; }
#image-thumb, #chip-thumb, #template-image { background:#f1f5f9; }
#session-thumb { background:#eef2ff; color:#64748b; }
QScrollBar:vertical { background:#f6f8fb; width:5px; border-radius:2px; }
QScrollBar::handle:vertical { background:#cbd5e1; border-radius:2px; min-height:24px; }
QScrollBar::handle:vertical:hover { background:#94a3b8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QScrollBar:horizontal { background:#f6f8fb; height:5px; border-radius:2px; }
QScrollBar::handle:horizontal { background:#cbd5e1; border-radius:2px; min-width:24px; }
QScrollBar::handle:horizontal:hover { background:#94a3b8; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width:0; }
QStatusBar { background:#ffffff; color:#64748b; font-size:11px; border-top:1px solid #e2e8f0; }
QProgressBar { background:#e2e8f0; }
QMessageBox { background:#ffffff; color:#111827; }
QDialog { background:#ffffff; }
QDialog QLabel { color:#334155; }
QLineEdit, QComboBox, QSpinBox { background:#ffffff; border:1px solid #dbe2ea; color:#111827; }
#header-action-btn { background:#ffffff; border:1px solid #dbe2ea; color:#475569; }
#header-action-btn:hover { background:#eef2ff; color:#312e81; border-color:#7c3aed; }
"""

STYLE = DARK_STYLE
THEME_STYLES = {"dark": DARK_STYLE, "light": LIGHT_STYLE}


def apply_app_palette(app, theme: str) -> None:
    colors = {
        "dark": {
            QPalette.ColorRole.Window: "#0b0d12",
            QPalette.ColorRole.WindowText: "#e8e8e8",
            QPalette.ColorRole.Base: "#0d111a",
            QPalette.ColorRole.AlternateBase: "#121722",
            QPalette.ColorRole.ToolTipBase: "#161616",
            QPalette.ColorRole.ToolTipText: "#dddddd",
            QPalette.ColorRole.Text: "#e8e8e8",
            QPalette.ColorRole.Button: "#151923",
            QPalette.ColorRole.ButtonText: "#cbd5e1",
            QPalette.ColorRole.BrightText: "#ff4040",
            QPalette.ColorRole.Link: "#7c3aed",
            QPalette.ColorRole.Highlight: "#7c3aed",
            QPalette.ColorRole.HighlightedText: "#ffffff",
        },
        "light": {
            QPalette.ColorRole.Window: "#f6f8fb",
            QPalette.ColorRole.WindowText: "#111827",
            QPalette.ColorRole.Base: "#ffffff",
            QPalette.ColorRole.AlternateBase: "#f8fafc",
            QPalette.ColorRole.ToolTipBase: "#ffffff",
            QPalette.ColorRole.ToolTipText: "#111827",
            QPalette.ColorRole.Text: "#111827",
            QPalette.ColorRole.Button: "#ffffff",
            QPalette.ColorRole.ButtonText: "#334155",
            QPalette.ColorRole.BrightText: "#b91c1c",
            QPalette.ColorRole.Link: "#6d28d9",
            QPalette.ColorRole.Highlight: "#ddd6fe",
            QPalette.ColorRole.HighlightedText: "#111827",
        },
    }.get(theme, {})
    palette = QPalette()
    for role, color in colors.items():
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
    app.setProperty("theme", theme)
