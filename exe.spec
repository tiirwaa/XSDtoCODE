# Análisis para el script GUI
a_gui = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[  # Datos específicos para la GUI
        ('logo.png', '.'),
        ('iconogui.ico', '.'),
        ('iconomain.ico', '.'),
        ('jdk1.8.0_202', 'jdk1.8.0_202'),
        ('csharp', 'csharp'),
        ('.venv/Lib/site-packages/xsdata/formats/dataclass/templates', 'xsdata/formats/dataclass/templates'),
        ('.venv/Scripts/ruff.exe', 'bin')
    ],
    hiddenimports=['xsdata', 'click', 'jinja2', 'toposort', 'docformatter', 'ruff', 'typing-extensions'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# EXE para GUI (ventana sin consola)
pyz_gui = PYZ(a_gui.pure)
exe_gui = EXE(
    pyz_gui,
    a_gui.scripts,
    [],
    exclude_binaries=True,
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No consola
    icon='iconogui.ico',  # <- ESTA LÍNEA AGREGA EL ÍCONO
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Análisis para el script MAIN (consola)
a_main = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],  # Datos específicos para la consola
    hiddenimports=['xsdata', 'click', 'jinja2', 'toposort', 'docformatter', 'ruff', 'typing-extensions'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# EXE para MAIN (consola)
pyz_main = PYZ(a_main.pure)
exe_main = EXE(
    pyz_main,
    a_main.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Consola
    icon='iconomain.ico',  # <- ESTA LÍNEA AGREGA EL ÍCONO
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Recolectar todo el contenido para la distribución (JUNTOS)
coll = COLLECT(
    exe_gui,
    exe_main,
    a_gui.binaries + a_main.binaries,
    a_gui.datas + a_main.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='XSDtoCODE',
)

# Finalización del proceso de compilación, con las colecciones separadas.
