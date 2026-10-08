# -*- coding: utf-8 -*-
"""Rebuild the whole site: python3 src/build_all.py  →  site/ (self-hosted) and artifact/ (claude.ai)."""
import os, subprocess, sys

SRC = os.path.dirname(os.path.abspath(__file__))
for script in ('odyssey/build.py', 'iliad/build_il.py', 'aeneid/build_ae.py', 'journey/build_xy.py', 'sanguo/build_sg.py',
               'honglou/build_hl.py', 'got/build_got.py', 'index/build_index.py'):
    subprocess.run([sys.executable, os.path.join(SRC, script)], check=True)
