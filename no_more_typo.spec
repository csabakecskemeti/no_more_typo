# -*- mode: python ; coding: utf-8 -*-

# Enhanced no_more_typo PyInstaller spec file
# Builds standalone executable with all dependencies

a = Analysis(
    ['no_more_typo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # LangChain dependencies
        'langchain',
        'langchain_community',
        'langchain_core',
        'langchain_openai',
        # Enhanced processor modules
        'enhanced_processor',
        'command_parser', 
        'prompt_templates',
        # Core dependencies
        'pyperclip',
        'pynput',
        'pynput.keyboard',
        'pynput._util',
        'pynput._util.darwin',
        # Standard library modules that might be missed
        'warnings',
        'sys',
        'os',
        're',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test modules from final executable
        'pytest',
        'test_command_parser',
        'test_prompt_templates', 
        'test_enhanced_processor',
        'test_integration',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='no_more_typo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for user feedback
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Additional metadata
    version_file=None,
    icon=None,  # Could add icon later
)
