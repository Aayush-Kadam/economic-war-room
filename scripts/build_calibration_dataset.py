"""Run the existing frozen-sample builder after official retrieval."""
from __future__ import annotations
import runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/"calibration/build_frozen_sample.py"),run_name="__main__")
