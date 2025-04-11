# -*- mode: python ; coding: utf-8 -*-
from tkinterdnd2 import TkinterDnD
import tkinterdnd2
import os

# tkinterdnd2 경로 찾기
tkdnd_path = os.path.join(os.path.dirname(tkinterdnd2.__file__), "tkdnd")

datas = [
    (tkdnd_path, "tkinterdnd2/tkdnd"),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SharedParameterViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
