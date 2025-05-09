# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['chatbot_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('skygem_icon.png', '.')],
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
    [],
    exclude_binaries=True,
    name='SkyGem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['skygem_icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SkyGem',
)
app = BUNDLE(
    coll,
    name='SkyGem.app',
    icon='skygem_icon.icns',
    bundle_identifier='com.shahzebali.skygem',
)
