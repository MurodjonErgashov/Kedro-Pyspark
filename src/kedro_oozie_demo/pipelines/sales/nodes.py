"""Thin executors that run the sales bronze/silver/gold notebooks.

The read/transform/write logic lives in `notebooks/sales/`, not here --
these functions only run a notebook and hand a sentinel value to the next
node so Kedro's pipeline enforces the run order.
"""

from kedro_oozie_demo.notebook_runner import run_notebook


def run_raw_to_bronze() -> str:
    run_notebook("sales", "01_raw_to_bronze.ipynb")
    return "done"


def run_bronze_to_silver(_raw_to_bronze_done: str) -> str:
    run_notebook("sales", "02_bronze_to_silver.ipynb")
    return "done"


def run_silver_to_gold(_bronze_to_silver_done: str) -> None:
    run_notebook("sales", "03_silver_to_gold.ipynb")
