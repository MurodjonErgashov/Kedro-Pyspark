# kedro_oozie_demo

A Kedro project with three independent bronze/silver/gold pipelines, where
the transformation logic lives in notebooks and Kedro just sequences them.
Each pipeline has its own raw source (a different file format each) but
they share the same `data/02_bronze`, `data/03_silver`, `data/04_gold`
folders -- one file per domain.

```
notebooks/00_config.ipynb   -- bootstraps the Kedro catalog, shared constants
notebooks/00_utils.ipynb    -- small reusable helper functions

notebooks/employees/   raw_employees (Excel) -> bronze -> silver -> gold_employees
notebooks/sales/       raw_sales     (CSV)   -> bronze -> silver -> gold_sales
notebooks/inventory/   raw_inventory (JSON)  -> bronze -> silver -> gold_inventory
```

Every stage notebook starts with `%run ../00_config.ipynb` (and
`%run ../00_utils.ipynb` where needed) to pull in the shared `catalog` object
and helpers, then reads its input and writes its output via
`catalog.load(...)` / `catalog.save(...)` -- the actual pandas transformation
code lives directly in the notebook's cells, not wrapped in Python functions.
Each notebook also has a "PySpark alternative (reference only)" section at
the bottom, fully commented out since PySpark isn't installed in this image --
left there to show what switching to Spark would look like.

None of the three `src/kedro_oozie_demo/pipelines/<name>/nodes.py` files
contain transformation logic. Each function there just executes one notebook
with [papermill](https://papermill.readthedocs.io/), via the shared
`notebook_runner.run_notebook()` helper, and passes a sentinel value to the
next node so each pipeline's `pipeline.py` enforces its own
raw -> bronze -> silver -> gold ordering. `kedro run` runs all three
pipelines' notebooks in place, and their executed cell outputs are saved
back to the `.ipynb` files.

## Run it

Build and run in Docker (no local Python setup needed):

```
docker build -t kedro-oozie-demo:latest .
docker run --rm -v "$(pwd)/data":/app/data -v "$(pwd)/notebooks":/app/notebooks kedro-oozie-demo:latest
```

Or from the repo root, use the wrapper script that also doubles as the
Oozie shell action's entry point:

```
../scripts/run_pipeline.sh
```

This runs all three pipelines. To run just one, e.g. sales:

```
docker run --rm -v "$(pwd)/data":/app/data -v "$(pwd)/notebooks":/app/notebooks kedro-oozie-demo:latest kedro run --pipeline sales
```

## Viewing the execution flow

`kedro viz run` launches a browser UI showing the pipelines as a DAG:

```
../scripts/run_viz.sh
```

Then open `http://127.0.0.1:4141`. Note it only shows the notebook-executor
nodes and the sentinel values chaining them within each pipeline
(e.g. `employees_raw_to_bronze_notebook -> employees_raw_to_bronze_done -> ...`),
not the real `raw_employees -> bronze_employees -> silver_employees ->
gold_employees` data lineage -- those catalog reads/writes happen inside the
notebooks, invisible to Kedro's pipeline graph.

## Editing the notebooks interactively

`kedro jupyter lab` launches Jupyter Lab so you can open and edit the stage
notebooks directly, re-running cells against real data:

```
../scripts/run_notebook.sh
```

Then open the printed `http://127.0.0.1:8888/lab?token=...` URL. The whole
project directory is mounted live, so edits made in the browser or your IDE
show up on both sides immediately.

## Scheduling

This project doesn't run a live Oozie server. The `../oozie/` folder holds
the workflow/coordinator XML that documents the intended production
schedule (daily at 02:00 GST) and is ready to submit to a real Oozie
server later.
