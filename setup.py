from setuptools import setup

APP = ['roast.py']
DATA_FILES = [
    ('models', ['models/glados.onnx'])
    ]

OPTIONS = {
    'argv_emulation': False,
    'frameworks': ['./venv/lib/python3.10/site-packages/_sounddevice_data/portaudio-binaries/libportaudio.dylib'],
    'iconfile': 'icon.icns'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
