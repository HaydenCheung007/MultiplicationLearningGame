# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)
from kivy_deps import sdl2, glew, gstreamer
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/*.kv', '.'),('assets/icons/*.png*.png', 'images'),('assets/numpad/*.png', 'images'),('assets/audio/challenge.mp3', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins +  gstreamer.dep_bins)],
    name='main',
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
