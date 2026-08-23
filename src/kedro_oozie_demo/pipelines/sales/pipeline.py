"""Sequences the sales bronze/silver/gold notebooks.

Kedro only manages *when* each notebook runs -- the sentinel strings passed
between nodes below exist purely to force run order; the actual data flows
through the catalog inside each notebook.
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import run_bronze_to_silver, run_raw_to_bronze, run_silver_to_gold


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=run_raw_to_bronze,
                inputs=None,
                outputs="sales_raw_to_bronze_done",
                name="sales_raw_to_bronze_notebook",
            ),
            node(
                func=run_bronze_to_silver,
                inputs="sales_raw_to_bronze_done",
                outputs="sales_bronze_to_silver_done",
                name="sales_bronze_to_silver_notebook",
            ),
            node(
                func=run_silver_to_gold,
                inputs="sales_bronze_to_silver_done",
                outputs=None,
                name="sales_silver_to_gold_notebook",
            ),
        ]
    )
