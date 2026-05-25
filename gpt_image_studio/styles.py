DARK_STYLE = """
* { font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif; }
QMainWindow, QWidget { background-color: #0b0d12; color: #e8e8e8; }

#sidebar { background: #0f1117; border-right: 1px solid #202431; }
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

#prompt-card { background:#121722; border:1px solid #293144; border-radius:18px; }
QTextEdit#prompt-input {
    background:#0d111a; border:1px solid #252b3a; border-radius:14px; color:#f8fafc;
    font-size:14px; padding:10px 12px; selection-background-color:#4c1d95;
}
QTextEdit#prompt-input:focus { border-color:#7c3aed; }

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

#session-item { background:#141925; border:1px solid #252b3a; border-radius:14px; margin:2px 8px; }
#session-item:hover { border-color:#475569; background:#192132; }
#session-item-active { background:#211638; border:1px solid #7c3aed; border-radius:14px; margin:2px 8px; }

#turn-frame { background:#121722; border-radius:16px; border:1px solid #252b3a; }
#turn-prompt { color:#e5e7eb; font-size:13px; }
#turn-meta { color:#64748b; font-size:11px; }

#img-card { background:#111827; border:1px solid #273244; border-radius:14px; }
#img-card:hover { border-color:#475569; }
#template-card { background:#111827; border:1px solid #273244; border-radius:16px; }
#template-card:hover { border-color:#7c3aed; background:#151c2b; }
#result-card { background:#121722; border:1px solid #252b3a; border-radius:18px; }

QScrollBar:vertical { background:#0b0d12; width:5px; border-radius:2px; }
QScrollBar::handle:vertical { background:#2e2e2e; border-radius:2px; min-height:24px; }
QScrollBar::handle:vertical:hover { background:#444; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QScrollBar:horizontal { background:#0b0d12; height:5px; border-radius:2px; }
QScrollBar::handle:horizontal { background:#2e2e2e; border-radius:2px; min-width:24px; }
QScrollBar::handle:horizontal:hover { background:#444; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width:0; }

QStatusBar { background:#0f0f0f; color:#555; font-size:11px; border-top:1px solid #1a1a1a; }
QProgressBar { background:#1e1e1e; border:none; border-radius:2px; height:3px; }
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7b2ff7,stop:1 #00b4d8);
    border-radius:2px;
}
QPushButton { font-size:13px; }
QMessageBox { background:#1a1a1a; color:#e0e0e0; }
QDialog { background:#181818; }
QDialog QLabel { color:#ccc; }
QLineEdit {
    background:#222; border:1px solid #2e2e2e; border-radius:7px;
    color:#e8e8e8; padding:6px 10px; font-size:13px;
}
QLineEdit:focus { border-color:#7b2ff7; }

#header-action-btn {
    background:#151923; border:1px solid #252b3a; border-radius:12px;
    color:#cbd5e1; font-size:12px; font-weight:700; padding:7px 12px;
}
#header-action-btn:hover { background:#1b2130; color:#f8fafc; border-color:#7c3aed; }
"""

LIGHT_STYLE = DARK_STYLE + """
QMainWindow, QWidget { background-color: #f6f8fb; color: #111827; }
#sidebar { background: #ffffff; border-right: 1px solid #dbe2ea; }
#brand-title { color:#111827; }
#brand-subtitle, #section-title { color:#64748b; }
#sidebar-tab { background:#f8fafc; border-color:#e2e8f0; color:#475569; }
#sidebar-tab:hover { background:#eef2ff; color:#111827; border-color:#c7d2fe; }
#sidebar-tab-active { background:#ede9fe; border-color:#7c3aed; color:#312e81; }
#sidebar-footer-btn { background:#f8fafc; border-color:#e2e8f0; color:#475569; }
#sidebar-footer-btn:hover { background:#eef2ff; color:#111827; border-color:#c7d2fe; }
#prompt-card, #result-card, #turn-frame { background:#ffffff; border-color:#dbe2ea; }
QTextEdit#prompt-input { background:#f8fafc; border-color:#dbe2ea; color:#111827; }
#template-card, #img-card { background:#ffffff; border-color:#dbe2ea; }
#template-card:hover, #img-card:hover { background:#f8fafc; border-color:#7c3aed; }
#session-item { background:#ffffff; border-color:#e2e8f0; }
#session-item:hover { background:#f8fafc; border-color:#cbd5e1; }
#session-item-active { background:#ede9fe; border-color:#7c3aed; }
#turn-prompt { color:#111827; }
#turn-meta { color:#64748b; }
#header-action-btn { background:#ffffff; border-color:#dbe2ea; color:#475569; }
#header-action-btn:hover { background:#eef2ff; color:#312e81; border-color:#7c3aed; }
QStatusBar { background:#ffffff; color:#64748b; border-top:1px solid #e2e8f0; }
QLineEdit { background:#ffffff; border-color:#dbe2ea; color:#111827; }
QDialog { background:#ffffff; }
QDialog QLabel { color:#334155; }
"""

STYLE = DARK_STYLE
THEME_STYLES = {"dark": DARK_STYLE, "light": LIGHT_STYLE}
