"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
Packages = ['pylogrus','requests', 'urllib3']
APP = ['main.py']
DATA_FILES = [('',["config"])]
OPTIONS = {
    'packages': ['requests'],
    "iconfile": 'datadog.icns',
    "plist": {
    'NSPrincipalClass': 'NSApplication',
    'CFBundleDisplayName': 'Datadog Intrusion Detection',
    'CFBundleIdentifier': 'com.datadog.intrustiondetection',
    'CFBundleInfoDictionaryVersion': '6.0',
    'CFBundleTypeIconFile': 'datadog.icns',
    'LSItemContentTypes': ['com.datadog.intrustiondetection'],
    'LSHandlerRank': 'Owner',
    'NSHumanReadableCopyright': 'Copyright (c) All rights reserved.',
    'CFBundleShortVersionString': '1.0.0',
        }
    }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=Packages,
    packages=['cogs']
)
