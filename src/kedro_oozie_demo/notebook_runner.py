"""Shared helper for running a pipeline's stage notebooks via papermill."""

from pathlib import Path

import papermill as pm

NOTEBOOKS_ROOT = Path(__file__).resolve().parents[2] / "notebooks"


def run_notebook(pipeline_name: str, notebook_name: str) -> None:
    notebooks_dir = NOTEBOOKS_ROOT / pipeline_name
    notebook_path = notebooks_dir / notebook_name
    pm.execute_notebook(
        str(notebook_path),
        str(notebook_path),
        cwd=str(notebooks_dir),
    )
