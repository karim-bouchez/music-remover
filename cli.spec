# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        (
            "pretrained_models",
            "pretrained_models"
        ),
        (
            "ff*",
            "."
        ),
        # TODO: use hook for this because path can defer
        (
            ".venv/lib/python3.8/site-packages/librosa",
            "librosa"
        ),
        (
            ".venv/lib/python3.8/site-packages/spleeter",
            "spleeter"
        )
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='music_remover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)