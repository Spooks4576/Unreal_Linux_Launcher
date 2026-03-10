#!/usr/bin/env python3
"""
Unreal Engine Launcher for Linux
Requires: sudo apt install python3-pyqt6
"""

import os
import sys
import json
import subprocess
import threading
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QFrame, QComboBox, QProgressBar, QScrollArea,
    QSizePolicy, QGroupBox, QLineEdit, QTextEdit,
    QStatusBar,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QPalette, QPixmap

STYLE = """
QMainWindow {
    background-color: #0d0e11;
}

QWidget {
    background-color: #0d0e11;
    color: #e8e6e0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 13px;
}

#sidebar {
    background-color: #111318;
    border-right: 1px solid #1e2128;
    min-width: 260px;
    max-width: 260px;
}

#sidebarHeader {
    background-color: #0a0b0d;
    border-bottom: 1px solid #1e2128;
}

#logoLabel {
    color: #e8e6e0;
    font-size: 11px;
    letter-spacing: 4px;
    font-weight: bold;
    padding: 20px 16px 4px 16px;
}

#versionLabel {
    color: #4a5568;
    font-size: 10px;
    letter-spacing: 2px;
    padding: 0px 16px 16px 16px;
}

QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
    padding: 4px 0px;
}

QListWidget::item {
    padding: 10px 14px;
    border-left: 3px solid transparent;
    color: #8a8f9e;
}

QListWidget::item:selected {
    background-color: #171920;
    border-left: 3px solid #c8a84b;
    color: #e8e6e0;
}

QListWidget::item:hover:!selected {
    background-color: #13151a;
    color: #b0b5c3;
    border-left: 3px solid #2a2e38;
}

#mainContent {
    background-color: #0d0e11;
}

#contentHeader {
    background-color: #0f1013;
    border-bottom: 1px solid #1a1d24;
    padding: 20px 28px;
}

#projectTitle {
    font-size: 22px;
    font-weight: bold;
    color: #e8e6e0;
    letter-spacing: 1px;
}

#projectPath {
    font-size: 11px;
    color: #4a5568;
    font-family: 'JetBrains Mono', monospace;
}

QPushButton {
    background-color: #1a1d24;
    color: #9aa0b0;
    border: 1px solid #252931;
    border-radius: 4px;
    padding: 9px 18px;
    font-size: 12px;
    letter-spacing: 1px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1e2229;
    color: #c8ccd6;
    border: 1px solid #353b47;
}

QPushButton:pressed {
    background-color: #13151a;
}

#launchBtn {
    background-color: #c8a84b;
    color: #0d0e11;
    border: none;
    padding: 11px 28px;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: bold;
    border-radius: 3px;
}

#launchBtn:hover {
    background-color: #d4b55a;
}

#launchBtn:pressed {
    background-color: #b8982e;
}

#launchBtn:disabled {
    background-color: #2a2d35;
    color: #454952;
}

#compileBtn {
    background-color: #1a2a1a;
    color: #5aaa5a;
    border: 1px solid #2a4a2a;
    padding: 11px 20px;
    letter-spacing: 1.5px;
    font-size: 11px;
    border-radius: 3px;
}

#compileBtn:hover {
    background-color: #1e341e;
    color: #7acc7a;
    border: 1px solid #3a6a3a;
}

#compileBtn:pressed {
    background-color: #141e14;
}

#compileBtn:disabled {
    background-color: #13151a;
    color: #2a402a;
    border: 1px solid #1a2a1a;
}

#genBtn {
    background-color: #1e2229;
    color: #7a8494;
    border: 1px solid #2a2e38;
    padding: 11px 20px;
    letter-spacing: 1.5px;
    font-size: 11px;
    border-radius: 3px;
}

#genBtn:hover {
    background-color: #252930;
    color: #9aa0b0;
    border: 1px solid #363d4a;
}

#patchBtn {
    background-color: #1a2030;
    color: #5a7aaa;
    border: 1px solid #253050;
    padding: 8px 16px;
    letter-spacing: 1.5px;
    font-size: 11px;
    border-radius: 3px;
}

#patchBtn:hover {
    background-color: #1e2840;
    color: #7a9acc;
    border: 1px solid #304060;
}

#patchBtn:disabled {
    background-color: #13151a;
    color: #2a3040;
    border: 1px solid #1a1d24;
}

#scanBtn {
    background-color: transparent;
    color: #5a6070;
    border: 1px solid #1e2128;
    font-size: 11px;
    letter-spacing: 1.5px;
    padding: 7px 14px;
    border-radius: 3px;
}

#scanBtn:hover {
    background-color: #13151a;
    color: #7a8090;
    border: 1px solid #252931;
}

QComboBox {
    background-color: #13151a;
    border: 1px solid #252931;
    border-radius: 3px;
    padding: 8px 12px;
    color: #9aa0b0;
    font-size: 12px;
    min-width: 200px;
}

QComboBox:hover {
    border: 1px solid #353b47;
    color: #c0c5d0;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    width: 8px;
    height: 8px;
    border-left: 2px solid #5a6070;
    border-bottom: 2px solid #5a6070;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #13151a;
    border: 1px solid #252931;
    color: #9aa0b0;
    selection-background-color: #1e2229;
    selection-color: #c8ccd6;
    outline: none;
}

#sectionLabel {
    font-size: 10px;
    color: #3a4050;
    letter-spacing: 3px;
    padding: 14px 16px 6px 16px;
    font-weight: bold;
}

QStatusBar {
    background-color: #0a0b0d;
    border-top: 1px solid #1a1d24;
    color: #3a4050;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 2px 8px;
}

QTextEdit {
    background-color: #0a0b0d;
    border: 1px solid #1a1d24;
    color: #5a6478;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    border-radius: 3px;
    padding: 8px;
}

QLineEdit {
    background-color: #111318;
    border: 1px solid #1e2128;
    border-radius: 3px;
    padding: 8px 12px;
    color: #8a8f9e;
    font-size: 12px;
}

QLineEdit:focus {
    border: 1px solid #2e3440;
    color: #b0b5c3;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #1e2229;
    border-radius: 3px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #2a2e38;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: transparent;
    height: 6px;
}

QScrollBar::handle:horizontal {
    background: #1e2229;
    border-radius: 3px;
}

#separator {
    background-color: #1a1d24;
    max-height: 1px;
    min-height: 1px;
}

QGroupBox {
    border: 1px solid #1a1d24;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 8px;
    color: #3a4050;
    font-size: 10px;
    letter-spacing: 2px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;
}

QProgressBar {
    background-color: #111318;
    border: none;
    border-radius: 2px;
    height: 3px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #c8a84b;
    border-radius: 2px;
}

#projectThumbnail {
    border: 1px solid #1a1d24;
    border-radius: 3px;
    background-color: #0a0b0d;
}

#thumbnailPlaceholder {
    background-color: #0f1115;
    border: 1px solid #1a1d24;
    border-radius: 3px;
    color: #2a2e38;
    font-size: 10px;
    letter-spacing: 2px;
}
"""


class ScannerThread(QThread):
    engine_found  = pyqtSignal(dict)
    project_found = pyqtSignal(dict)
    scan_complete = pyqtSignal(int, int)
    status_update = pyqtSignal(str)

    SKIP_DIRS = {
        '.git', 'node_modules', '__pycache__', '.cache', '.local',
        '.mozilla', '.config', '.steam', 'snap', 'proc', 'sys',
        'Saved', 'Intermediate', 'DerivedDataCache', '.vscode',
        '.idea', 'Build', 'Binaries',
    }

    def run(self):
        home = Path.home()
        self._engine_roots: set[Path] = set()

        self.status_update.emit("Scanning for Unreal Engine installations...")
        engines = self._find_engines(home)

        self.status_update.emit(
            f"Found {len(engines)} engine(s). Scanning for projects..."
        )
        projects = self._find_projects(home)

        self.scan_complete.emit(len(engines), len(projects))

    def _find_engines(self, root: Path) -> list:
        found: list[dict] = []
        self._walk_for_engines(root, found, depth=0, max_depth=5)
        return found

    def _walk_for_engines(self, path: Path, found: list, depth: int, max_depth: int):
        if depth > max_depth:
            return
        try:
            for entry in path.iterdir():
                if not entry.is_dir():
                    continue
                if entry.name in self.SKIP_DIRS or entry.name.startswith('.'):
                    continue
                info = self._check_engine_dir(entry)
                if info:
                    found.append(info)
                    self._engine_roots.add(entry.resolve())
                    self.engine_found.emit(info)
                else:
                    self._walk_for_engines(entry, found, depth + 1, max_depth)
        except (PermissionError, OSError):
            pass

    def _check_engine_dir(self, path: Path) -> dict | None:
        ue_binary    = path / "Engine" / "Binaries" / "Linux" / "UnrealEditor"
        ue4_binary   = path / "Engine" / "Binaries" / "Linux" / "UE4Editor"
        build_sh     = path / "Engine" / "Build" / "BatchFiles" / "Linux" / "Build.sh"
        setup_sh     = path / "Setup.sh"
        version_file = path / "Engine" / "Build" / "Build.version"

        is_engine = (
            ue_binary.exists() or
            ue4_binary.exists() or
            (build_sh.exists() and setup_sh.exists())
        )
        if not is_engine:
            return None

        version_str = "Unknown"
        major = 0
        if version_file.exists():
            try:
                data = json.loads(version_file.read_text())
                major       = data.get("MajorVersion", 0)
                minor       = data.get("MinorVersion", 0)
                patch       = data.get("PatchVersion", 0)
                version_str = f"{major}.{minor}.{patch}"
            except Exception:
                pass

        if version_str == "Unknown":
            if ue4_binary.exists():
                major, version_str = 4, "4.x"
            elif ue_binary.exists():
                major, version_str = 5, "5.x"

        binary = str(ue_binary) if ue_binary.exists() else str(ue4_binary)
        label  = f"UE{major} {version_str}" if major else f"UE {version_str}"

        return {
            "path":    str(path),
            "version": version_str,
            "major":   major,
            "label":   label,
            "binary":  binary,
        }

    def _find_projects(self, root: Path) -> list:
        found: list[dict] = []
        self._walk_for_projects(root, found, depth=0, max_depth=6)
        return found

    def _is_inside_engine(self, path: Path) -> bool:
        try:
            resolved = path.resolve()
            for engine_root in self._engine_roots:
                if resolved == engine_root or engine_root in resolved.parents:
                    return True
        except OSError:
            pass
        return False

    def _walk_for_projects(self, path: Path, found: list, depth: int, max_depth: int):
        if depth > max_depth:
            return
        if self._is_inside_engine(path):
            return
        try:
            for entry in path.iterdir():
                if entry.is_file() and entry.suffix == ".uproject":
                    info = self._parse_uproject(entry)
                    found.append(info)
                    self.project_found.emit(info)
                elif entry.is_dir():
                    if entry.name in self.SKIP_DIRS or entry.name.startswith('.'):
                        continue
                    self._walk_for_projects(entry, found, depth + 1, max_depth)
        except (PermissionError, OSError):
            pass

    def _parse_uproject(self, path: Path) -> dict:
        engine_association = category = description = ""
        try:
            data               = json.loads(path.read_text())
            engine_association = data.get("EngineAssociation", "")
            category           = data.get("Category", "")
            description        = data.get("Description", "")
        except Exception:
            pass
        return {
            "name":               path.stem,
            "path":               str(path),
            "dir":                str(path.parent),
            "engine_association": engine_association,
            "category":           category,
            "description":        description,
        }


class ProjectItem(QListWidgetItem):
    def __init__(self, project: dict):
        super().__init__()
        self.project = project
        self.setText(project["name"])
        self.setSizeHint(QSize(0, 46))


def _find_project_thumbnail(project_dir: str, project_name: str) -> str | None:
    base = Path(project_dir)
    candidates = [
        base / "Saved" / "AutoScreenshot.png",
        base / "Saved" / "Screenshots" / "WindowsNoEditor" / f"{project_name}.png",
        base / "Saved" / "Screenshots" / "LinuxNoEditor" / f"{project_name}.png",
        base / "Saved" / "Screenshots" / f"{project_name}.png",
        base / "Content" / "Splash" / "Splash.bmp",
        base / "Content" / "Splash" / "EdSplash.bmp",
    ]
    for ext in ("png", "jpg", "jpeg", "bmp"):
        candidates.append(base / f"{project_name}.{ext}")
        candidates.append(base / f"thumbnail.{ext}")
        candidates.append(base / f"preview.{ext}")

    for c in candidates:
        if c.exists():
            return str(c)
    return None


class ProjectDetailPanel(QWidget):
    launch_requested   = pyqtSignal(dict, dict)
    generate_requested = pyqtSignal(dict, dict)
    patch_requested    = pyqtSignal(dict, dict)
    compile_requested  = pyqtSignal(dict, dict)

    _log_signal    = pyqtSignal(str)
    _status_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mainContent")
        self.current_project: dict | None = None
        self.engines: list[dict] = []
        self._build_ui()
        self._log_signal.connect(self._append_log)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = QWidget()
        self.header.setObjectName("contentHeader")
        self.header.setFixedHeight(110)
        hl = QHBoxLayout(self.header)
        hl.setContentsMargins(28, 16, 28, 16)
        hl.setSpacing(18)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setObjectName("projectThumbnail")
        self.thumbnail_label.setFixedSize(128, 72)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setScaledContents(False)
        self._set_thumbnail_placeholder()
        hl.addWidget(self.thumbnail_label)

        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        self.title_label = QLabel("Select a project")
        self.title_label.setObjectName("projectTitle")
        self.path_label  = QLabel("")
        self.path_label.setObjectName("projectPath")
        title_block.addWidget(self.title_label)
        title_block.addWidget(self.path_label)
        title_block.addStretch()
        hl.addLayout(title_block, 1)

        layout.addWidget(self.header)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        body = QWidget()
        body.setObjectName("mainContent")
        self.body_layout = QVBoxLayout(body)
        self.body_layout.setContentsMargins(28, 24, 28, 24)
        self.body_layout.setSpacing(16)

        engine_row = QHBoxLayout()
        engine_row.setSpacing(12)
        engine_lbl = QLabel("ENGINE")
        engine_lbl.setObjectName("sectionLabel")
        engine_lbl.setFixedWidth(80)
        self.engine_combo = QComboBox()
        self.engine_combo.setPlaceholderText("Select engine version...")
        self.engine_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        engine_row.addWidget(engine_lbl)
        engine_row.addWidget(self.engine_combo)
        self.body_layout.addLayout(engine_row)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        self.body_layout.addWidget(sep2)

        info_group = QGroupBox("PROJECT INFO")
        info_layout = QVBoxLayout(info_group)
        info_layout.setSpacing(8)
        self.category_lbl = QLabel("")
        self.category_lbl.setObjectName("projectPath")
        self.desc_lbl     = QLabel("")
        self.desc_lbl.setObjectName("projectPath")
        self.desc_lbl.setWordWrap(True)
        self.assoc_lbl    = QLabel("")
        self.assoc_lbl.setObjectName("projectPath")
        info_layout.addWidget(self._info_row("Category",    self.category_lbl))
        info_layout.addWidget(self._info_row("Association", self.assoc_lbl))
        info_layout.addWidget(self._info_row("Description", self.desc_lbl))
        self.body_layout.addWidget(info_group)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.launch_btn = QPushButton("▶  LAUNCH")
        self.launch_btn.setObjectName("launchBtn")
        self.launch_btn.setFixedHeight(42)
        self.launch_btn.clicked.connect(self._on_launch)
        self.launch_btn.setEnabled(False)

        self.compile_btn = QPushButton("⚒  COMPILE")
        self.compile_btn.setObjectName("compileBtn")
        self.compile_btn.setFixedHeight(42)
        self.compile_btn.clicked.connect(self._on_compile)
        self.compile_btn.setEnabled(False)

        self.gen_btn = QPushButton("⚙  GENERATE PROJECT FILES")
        self.gen_btn.setObjectName("genBtn")
        self.gen_btn.setFixedHeight(42)
        self.gen_btn.clicked.connect(self._on_generate)
        self.gen_btn.setEnabled(False)

        btn_layout.addWidget(self.launch_btn, 2)
        btn_layout.addWidget(self.compile_btn, 2)
        btn_layout.addWidget(self.gen_btn, 3)
        self.body_layout.addLayout(btn_layout)

        patch_layout = QHBoxLayout()
        patch_layout.setSpacing(10)
        self.patch_btn = QPushButton("⛓  FIX ENGINE ASSOCIATION IN .UPROJECT")
        self.patch_btn.setObjectName("patchBtn")
        self.patch_btn.setFixedHeight(34)
        self.patch_btn.setToolTip(
            "Writes the selected engine's path into the .uproject EngineAssociation field.\n"
            "Fixes 'Failed to locate Unreal Engine associated with the project file' errors."
        )
        self.patch_btn.clicked.connect(self._on_patch)
        self.patch_btn.setEnabled(False)
        patch_layout.addWidget(self.patch_btn)
        self.body_layout.addLayout(patch_layout)

        log_label = QLabel("OUTPUT LOG")
        log_label.setObjectName("sectionLabel")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(180)
        self.log_output.setPlaceholderText("// output will appear here")
        self.body_layout.addWidget(log_label)
        self.body_layout.addWidget(self.log_output)
        self.body_layout.addStretch()

        scroll.setWidget(body)
        layout.addWidget(scroll)

    def _set_thumbnail_placeholder(self):
        self.thumbnail_label.setObjectName("thumbnailPlaceholder")
        self.thumbnail_label.setText("NO PREVIEW")
        self.thumbnail_label.setStyleSheet(
            "color: #2a2e38; font-size: 9px; letter-spacing: 2px;"
            "background-color: #0f1115; border: 1px solid #1a1d24; border-radius: 3px;"
        )
        self.thumbnail_label.setPixmap(QPixmap())

    def _load_thumbnail(self, project: dict):
        thumb_path = _find_project_thumbnail(project["dir"], project["name"])
        if thumb_path:
            pixmap = QPixmap(thumb_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    128, 72,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                cropped = scaled.copy(
                    (scaled.width() - 128) // 2,
                    (scaled.height() - 72) // 2,
                    128, 72
                )
                self.thumbnail_label.setText("")
                self.thumbnail_label.setStyleSheet(
                    "border: 1px solid #1a1d24; border-radius: 3px; background-color: #0a0b0d;"
                )
                self.thumbnail_label.setPixmap(cropped)
                return
        self._set_thumbnail_placeholder()

    def _info_row(self, label_text: str, value_widget: QLabel) -> QWidget:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(12)
        lbl = QLabel(label_text + ":")
        lbl.setFixedWidth(90)
        lbl.setStyleSheet("color: #2e3440; font-size: 11px; letter-spacing: 1px;")
        row_layout.addWidget(lbl)
        row_layout.addWidget(value_widget, 1)
        return row

    def set_engines(self, engines: list):
        self.engines = engines
        self.engine_combo.clear()
        for e in engines:
            self.engine_combo.addItem(e["label"], e)
        if self.current_project:
            self._try_match_engine()

    def set_project(self, project: dict):
        self.current_project = project
        self.title_label.setText(project["name"])
        self.path_label.setText(project["path"])
        self.category_lbl.setText(project.get("category") or "—")
        self.desc_lbl.setText(project.get("description") or "—")
        self.assoc_lbl.setText(project.get("engine_association") or "—")
        self.launch_btn.setEnabled(True)
        self.gen_btn.setEnabled(True)
        self.patch_btn.setEnabled(True)
        self.compile_btn.setEnabled(True)
        self._try_match_engine()
        self._load_thumbnail(project)

    def log(self, text: str):
        self._log_signal.emit(text)

    def _append_log(self, text: str):
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def _try_match_engine(self):
        if not self.current_project or not self.engines:
            return
        assoc = self.current_project.get("engine_association", "").lower()
        if not assoc:
            return
        for i, e in enumerate(self.engines):
            if assoc in e["version"].lower() or assoc in e["label"].lower():
                self.engine_combo.setCurrentIndex(i)
                return

    def _get_selected_engine(self) -> dict | None:
        idx = self.engine_combo.currentIndex()
        if 0 <= idx < len(self.engines):
            return self.engines[idx]
        return None

    def _on_launch(self):
        engine = self._get_selected_engine()
        if not engine:
            self.log("ERROR: No engine selected.")
            return
        if self.current_project:
            self.launch_requested.emit(self.current_project, engine)

    def _on_generate(self):
        engine = self._get_selected_engine()
        if not engine:
            self.log("ERROR: No engine selected.")
            return
        if self.current_project:
            self.generate_requested.emit(self.current_project, engine)

    def _on_patch(self):
        engine = self._get_selected_engine()
        if not engine:
            self.log("ERROR: No engine selected.")
            return
        if self.current_project:
            self.patch_requested.emit(self.current_project, engine)

    def _on_compile(self):
        engine = self._get_selected_engine()
        if not engine:
            self.log("ERROR: No engine selected.")
            return
        if self.current_project:
            self.compile_requested.emit(self.current_project, engine)


class UELauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engines:  list[dict] = []
        self.projects: list[dict] = []
        self.scanner: ScannerThread | None = None
        self._build_ui()
        self._start_scan()

    def _build_ui(self):
        self.setWindowTitle("Unreal Launcher")
        self.setMinimumSize(1000, 680)
        self.resize(1200, 760)

        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("Ready — scanning on startup...")

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        header = QWidget()
        header.setObjectName("sidebarHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        logo_lbl = QLabel("UNREAL LAUNCHER")
        logo_lbl.setObjectName("logoLabel")
        ver_lbl = QLabel("FOR LINUX")
        ver_lbl.setObjectName("versionLabel")
        header_layout.addWidget(logo_lbl)
        header_layout.addWidget(ver_lbl)
        sidebar_layout.addWidget(header)

        top_controls = QWidget()
        top_controls.setStyleSheet("background: transparent;")
        tc_layout = QVBoxLayout(top_controls)
        tc_layout.setContentsMargins(10, 10, 10, 6)
        tc_layout.setSpacing(8)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Filter projects...")
        self.search_box.textChanged.connect(self._filter_projects)
        tc_layout.addWidget(self.search_box)
        scan_btn = QPushButton("↻  RESCAN")
        scan_btn.setObjectName("scanBtn")
        scan_btn.clicked.connect(self._start_scan)
        tc_layout.addWidget(scan_btn)
        sidebar_layout.addWidget(top_controls)

        engines_label = QLabel("ENGINES")
        engines_label.setObjectName("sectionLabel")
        sidebar_layout.addWidget(engines_label)
        self.engine_list = QListWidget()
        self.engine_list.setMaximumHeight(160)
        self.engine_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        sidebar_layout.addWidget(self.engine_list)

        projects_label = QLabel("PROJECTS")
        projects_label.setObjectName("sectionLabel")
        sidebar_layout.addWidget(projects_label)
        self.project_list = QListWidget()
        self.project_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.project_list.currentItemChanged.connect(self._on_project_selected)
        sidebar_layout.addWidget(self.project_list)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        sidebar_layout.addWidget(self.progress_bar)

        root.addWidget(sidebar)

        self.detail_panel = ProjectDetailPanel()
        self.detail_panel.launch_requested.connect(self._do_launch)
        self.detail_panel.generate_requested.connect(self._do_generate)
        self.detail_panel.patch_requested.connect(self._do_patch_association)
        self.detail_panel.compile_requested.connect(self._do_compile)
        self.detail_panel._status_signal.connect(self._status_bar.showMessage)
        root.addWidget(self.detail_panel, 1)

    def _start_scan(self):
        if self.scanner and self.scanner.isRunning():
            return
        self.engines.clear()
        self.projects.clear()
        self.engine_list.clear()
        self.project_list.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.scanner = ScannerThread()
        self.scanner.engine_found.connect(self._on_engine_found)
        self.scanner.project_found.connect(self._on_project_found)
        self.scanner.scan_complete.connect(self._on_scan_complete)
        self.scanner.status_update.connect(self._status_bar.showMessage)
        self.scanner.start()

    def _on_engine_found(self, engine: dict):
        self.engines.append(engine)
        major  = engine.get("major", 0)
        prefix = "UE5" if major >= 5 else "UE4"
        item   = QListWidgetItem(f"  {prefix} {engine['version']}")
        item.setData(Qt.ItemDataRole.UserRole, engine)
        item.setSizeHint(QSize(0, 40))
        self.engine_list.addItem(item)
        self.detail_panel.set_engines(self.engines)

    def _on_project_found(self, project: dict):
        self.projects.append(project)
        self.project_list.addItem(ProjectItem(project))

    def _on_scan_complete(self, engine_count: int, project_count: int):
        self.progress_bar.setVisible(False)
        self._status_bar.showMessage(
            f"Found {engine_count} engine installation(s)  ·  {project_count} project(s)"
        )

    def _on_project_selected(self, current: QListWidgetItem, _previous):
        if isinstance(current, ProjectItem):
            self.detail_panel.set_engines(self.engines)
            self.detail_panel.set_project(current.project)

    def _filter_projects(self, text: str):
        text = text.lower()
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            item.setHidden(text not in item.text().lower())

    def _do_launch(self, project: dict, engine: dict):
        binary   = engine.get("binary", "")
        uproject = project["path"]

        if not os.path.isfile(binary):
            binary = self._find_editor_binary(engine["path"])

        if not binary:
            self.detail_panel.log(
                f"ERROR: Could not find editor binary in {engine['path']}"
            )
            return

        self.detail_panel.log(f"Launching: {binary} \"{uproject}\"")
        self._status_bar.showMessage(f"Launching {project['name']}...")

        try:
            subprocess.Popen(
                [binary, uproject],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            self.detail_panel.log("✓ Launch command sent. Editor is starting...")
            self._status_bar.showMessage(f"Launched {project['name']}")
        except Exception as e:
            self.detail_panel.log(f"ERROR: {e}")

    def _do_generate(self, project: dict, engine: dict):
        engine_root = engine["path"]
        uproject    = project["path"]

        gen_script = self._find_gen_script(engine_root)
        if not gen_script:
            self.detail_panel.log(
                "ERROR: Could not find GenerateProjectFiles.sh in engine root."
            )
            return

        cmd = [gen_script, f"-project={uproject}", "-game", "-engine"]
        self.detail_panel.log(f"Running: {' '.join(cmd)}")
        self._status_bar.showMessage("Generating project files...")

        panel = self.detail_panel

        def run_in_thread():
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=engine_root,
                )
                output = (result.stdout + result.stderr).strip()
                for line in output.splitlines():
                    panel.log(line)
                if result.returncode == 0:
                    panel.log("✓ Project files generated successfully.")
                    panel._status_signal.emit("Project files generated.")
                else:
                    panel.log(f"✗ Process exited with code {result.returncode}")
                    panel._status_signal.emit("Generation failed — see output log.")
            except Exception as e:
                panel.log(f"ERROR: {e}")
                panel._status_signal.emit("Generation error.")

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _do_compile(self, project: dict, engine: dict):
        engine_root  = engine["path"]
        uproject     = project["path"]
        project_name = project["name"]

        build_script = self._find_build_script(engine_root)
        if not build_script:
            self.detail_panel.log(
                "ERROR: Could not find Build.sh in engine root.\n"
                "Expected: Engine/Build/BatchFiles/Linux/Build.sh"
            )
            return

        cmd = [
            build_script,
            f"{project_name}Editor",
            "Linux",
            "Development",
            uproject,
            "-waitmutex",
        ]

        self.detail_panel.log(f"Compiling: {' '.join(cmd)}")
        self._status_bar.showMessage(f"Compiling {project_name}...")

        panel  = self.detail_panel
        status = self._status_bar

        def run_in_thread():
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=engine_root,
                    bufsize=1,
                )
                for line in proc.stdout:
                    panel.log(line.rstrip())
                proc.wait()
                if proc.returncode == 0:
                    panel.log("✓ Compilation succeeded.")
                    panel._status_signal.emit(f"Compiled {project_name} successfully.")
                else:
                    panel.log(f"✗ Compilation failed (exit code {proc.returncode}).")
                    panel._status_signal.emit("Compilation failed — see output log.")
            except Exception as e:
                panel.log(f"ERROR: {e}")
                panel._status_signal.emit("Compilation error.")

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _do_patch_association(self, project: dict, engine: dict):
        import uuid as _uuid
        import configparser

        uproject_path = Path(project["path"])
        engine_path   = engine["path"]
        ini_path      = Path.home() / ".config" / "Epic" / "UnrealEngine" / "Install.ini"

        log = self.detail_panel.log

        config = configparser.RawConfigParser()
        config.optionxform = str

        if ini_path.exists():
            try:
                config.read(ini_path)
                log(f"Read existing Install.ini: {ini_path}")
            except Exception as e:
                log(f"WARNING: Could not parse Install.ini: {e} — will overwrite.")
        else:
            log(f"Install.ini not found — will create: {ini_path}")

        if not config.has_section("Installations"):
            config.add_section("Installations")

        existing_guid = None
        for key, val in config.items("Installations"):
            if Path(val).resolve() == Path(engine_path).resolve():
                existing_guid = key
                log(f"Found existing GUID for this engine: {key}")
                break

        if existing_guid:
            guid_str = existing_guid
        else:
            guid_str = "{" + str(_uuid.uuid4()).upper() + "}"
            config.set("Installations", guid_str, engine_path)
            log(f"Generated new GUID: {guid_str}")

        try:
            ini_path.parent.mkdir(parents=True, exist_ok=True)
            with ini_path.open("w") as f:
                config.write(f)
            log(f"✓ Wrote Install.ini  ({ini_path})")
            log(f"  {guid_str} = {engine_path}")
        except Exception as e:
            log(f"ERROR: Could not write Install.ini: {e}")
            return

        try:
            data = json.loads(uproject_path.read_text())
        except Exception as e:
            log(f"ERROR: Could not read .uproject: {e}")
            return

        old_assoc = data.get("EngineAssociation", "")
        data["EngineAssociation"] = guid_str

        try:
            uproject_path.write_text(json.dumps(data, indent="\t") + "\n")
        except Exception as e:
            log(f"ERROR: Could not write .uproject: {e}")
            return

        log(f"✓ Patched {uproject_path.name}")
        log(f"  EngineAssociation: \"{old_assoc}\"  →  \"{guid_str}\"")
        self._status_bar.showMessage(
            f"Association fixed — GUID {guid_str} → {engine_path}"
        )

        project["engine_association"] = guid_str
        self.detail_panel.assoc_lbl.setText(guid_str)

    def _find_editor_binary(self, engine_root: str) -> str:
        linux_bin = Path(engine_root) / "Engine" / "Binaries" / "Linux"
        for name in ("UnrealEditor", "UE4Editor", "UnrealEditor-Linux-Shipping"):
            p = linux_bin / name
            if p.exists():
                return str(p)
        return ""

    def _find_gen_script(self, engine_root: str) -> str:
        candidates = [
            Path(engine_root) / "GenerateProjectFiles.sh",
            Path(engine_root) / "Engine" / "Build" / "BatchFiles" / "Linux" / "GenerateProjectFiles.sh",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return ""

    def _find_build_script(self, engine_root: str) -> str:
        candidates = [
            Path(engine_root) / "Engine" / "Build" / "BatchFiles" / "Linux" / "Build.sh",
            Path(engine_root) / "Build.sh",
        ]
        for c in candidates:
            if c.exists():
                return str(c)
        return ""


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor("#0d0e11"))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor("#e8e6e0"))
    palette.setColor(QPalette.ColorRole.Base,            QColor("#111318"))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor("#13151a"))
    palette.setColor(QPalette.ColorRole.ToolTipBase,     QColor("#13151a"))
    palette.setColor(QPalette.ColorRole.ToolTipText,     QColor("#e8e6e0"))
    palette.setColor(QPalette.ColorRole.Text,            QColor("#e8e6e0"))
    palette.setColor(QPalette.ColorRole.Button,          QColor("#1a1d24"))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor("#9aa0b0"))
    palette.setColor(QPalette.ColorRole.BrightText,      QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor("#c8a84b"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#0d0e11"))
    app.setPalette(palette)

    window = UELauncher()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
